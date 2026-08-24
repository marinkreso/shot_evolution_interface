"""
UTR_match_metrics.py  (cv4)
===========================

cv4 = cv3 with the SERVE ATTEMPT RESOLUTION fix (see resolve_serve_attempts):
the raw `serve_number` counts every serve ROW the CV wrote down, so lets,
phantom 'Extra' detections and duplicated serve rows each eat a service
attempt and a genuine 1st serve can arrive labelled 2 (or 3). Every serve and
return population is now taken from the resolved `serve_attempt` /
`serve_outcome` columns instead of `(serve_number == sn) & is_shot_in`:

  * rallies that were never played (Let / Extra, and a serve that duplicates a
    later one in the same point — same placement, landing spot and speed) are
    dropped before attempts are numbered, and a point is capped at its last two
    attempts;
  * the attempt number is written onto EVERY row of the rally it opened, so
    returns and +1 shots inherit the corrected number for free;
  * in/out comes from the point structure — an attempt with a later attempt
    behind it was out, the last attempt was in unless the point ended on a
    Fault — rather than from `is_shot_in` on the serve row.
Re-resolving is a no-op on data that already went through it, so legacy parquet
dumps taken before the fix and freshly adapted frames both work.

cv3 = cv2 with TWO changes taken from utr_match_metrics_manual5newspeed_all.py:
  1. the "Movement & Footwork" block is the manual one (per-frame move_* columns
     when present, else the displacement-based get_speed / get_acceleration
     fallback) instead of cv2's per-run gather/median/p95 block;
  2. the "Big-Point & +1 Ratios" section is added at the end of the report
     (ratio_metric over the pressure/overall/+1 win% metrics; needs the
     return_win baseline, added alongside return_plus1_win but, as in the manual
     script, not reported on its own).
Everything else is cv2 verbatim; the now-unused run helpers are left in place so
the movement swap is easy to revert.

Compute the UTR "Feature List" metrics for a single player in a single match.

Input  : player_name + match_id + two dataframes
           serves_df   - every serve/return event across all points
           movement_df - rally shots for points with COMPLETE movement tracking
Output : a JSON object holding every metric in UTR_Feature_List.docx, with the
         document's own labels (e.g. "1st Serve In%"), computed for the player
         AND the opponent ("All metrics for players and opponents").

Dataframe routing (mirrors CalculationsFinal5's df_serve vs df split):
  serves_df   -> 1st/2nd Serve (all), Return (all), the +1 win metrics,
                 Pressure & Big Points, Overall Win%   (no tracking needed)
  movement_df -> Forehand, Backhand, Net, Rally, Movement & Footwork,
                 Court Position                         (rally-shot + tracking)
If only one dataframe is supplied it is used for both.

Data schema (mensik_fonseca parquet)
------------------------------------
Shot-level columns used:
  shot_no            1=serve, 2=return, 3=serve+1, 4=return+1, >=4 rally
  serve_number       1 / 2
  PLAYER_HIT         who hit the shot
  PLAYER_WIN_NAME    who won the point
  server_name / receiver_name
  is_shot_in         1.0 if the shot landed in
  shot_type          'F' forehand, 'B' backhand, 'U' serve/other
  SPEED              shot speed (MPH)
  REBOUND_X_abs      landing depth (m, from net); baseline ~11.89
  REBOUND_Y_mirrored landing width (m, lateral)
  CONTACT_X_abs      contact depth (m)
  CONTACT_Y_mirrored contact lateral (m): < -2 deuce, > 2 ad
  distance_from_side_or_center_line   serve accuracy (m to target line)
  is_break_point / is_pressure_point  0/1
  point_id, match_id, surface

Per-frame movement (every 0.02 s), stored as stringified arrays and tracked by
point ROLE (server vs returner), not by selected player:
  server_location_x / server_location_y
  returner_location_x / returner_location_y
For each point the selected player is mapped to the server or returner track via
server_name. A "run" is one of the player's own rally shots: the location track
for that row spans from the opponent's contact of the incoming ball (start) to
the player reaching the ball (end), sampled at dt = 0.02 s. Speed and
acceleration are each computed on the run with THREE per-run definitions, then
aggregated across runs as the MEDIAN and the 95th PERCENTILE (not the mean):
  Start-End : net displacement / elapsed time   (e.g. |x_end - x_start| / t)
  Max       : peak instantaneous value during the run
  Average   : mean of the per-sample instantaneous values
Axes (Hawk-Eye): longitudinal = x, lateral = y. Foot = Euclidean magnitude.

Besides the overall foot speed/acceleration, the block reports three directional
run categories, each gated on the INCOMING ball (the previous shot) and the
player's displacement to reach it (foot speed + foot acceleration per category):
  Right/Deuce : >= RUN_LATERAL_M m lateral toward the deuce side, incoming
                previous_shot_speed > RUN_INCOMING_KMH km/h.
  Left/Ad     : >= RUN_LATERAL_M m lateral toward the ad side, same speed gate.
  Dropshot    : >= DROP_NET_M m toward the net, incoming > DROP_INCOMING_KMH km/h,
                incoming bounce REBOUND_X_abs < DROP_REBOUND_X_MAX m and
                spinRPM < 0 (short, sliced ball).

The distance-moved columns describe movement AFTER a shot, so the movement to
REACH a shot is the PREVIOUS shot's value (rows are sorted by match_id, set_no,
game_no, point_no, serve_number, shot_no to make "previous shot" well defined).
Running/stationary splits and the "when running" filter use this distance-into-
shot vs RUNNING_DISTANCE_M.

-------------------------------------------------------------------------------
ASSUMPTIONS (edit CONFIG if your data differs)
-------------------------------------------------------------------------------
1. SPEED is MPH; distances/tracking coords are meters.
2. Movement values are converted m->ft (FOOT_SCALE) so foot speed is ft/s and
   acceleration ft/s^2; lateral/longitudinal speeds use the same ft/s unit.
   Set FOOT_SCALE = 1.0 to stay metric.
3. Hawk-Eye convention: longitudinal = x-direction, lateral = y-direction.
4. Running vs stationary uses the distance moved to reach the shot (the previous
   shot's distance-moved): > RUNNING_DISTANCE_M (3 m) is running, else stationary.
5. Baseline at BASELINE_X, singles sideline at SIDELINE_Y (absolute frame).
"""

import argparse
import ast
import json
import math
import os

import numpy as np
import pandas as pd

# ============================ CONFIG ========================================= #

FRAME_DT = 0.02
BASELINE_X = 11.89           # baseline distance from net (m); depth = REBOUND_X_abs - BASELINE_X
SIDELINE_Y = 4.12            # singles sideline (m); width = |SIDELINE_Y - |REBOUND_Y_mirrored||
VOLLEY_CONTACT_X_MAX = 7.5   # a volley is contacted inside this depth (m) with no bounce
DEUCE_SIDE_Y = -2.0
AD_SIDE_Y = 2.0
RALLY_MIN_SHOT_NO = 4

RUNNING_DISTANCE_M = 3.0     # distance moved to reach a shot: > 3 m running, <= 3 m stationary

# --- directional "running shot" categories (Movement & Footwork) ------------- #
RUN_LATERAL_M = 2.5          # lateral displacement into the shot (m) that marks a wide run
RUN_INCOMING_KMH = 100.0     # incoming ball (previous_shot_speed) must exceed this (km/h)
DROP_NET_M = 3.0             # toward-the-net displacement into a dropshot (m)
DROP_INCOMING_KMH = 70.0     # incoming ball speed must exceed this for a dropshot run (km/h)
DROP_REBOUND_X_MAX = 7.4     # incoming ball bounced closer than this to the net (m) = short
DROP_SPIN_MAX = 0.0          # incoming ball spinRPM below this = slice/backspin (dropshot)
# In the mirrored frame (as in CONTACT_Y_mirrored) the deuce/right side is
# negative Y and the ad/left side is positive Y. Flip this sign if your tracking
# frame is oriented the other way (right/deuce runs would otherwise read as left/ad).
DEUCE_SIDE_SIGN = -1.0

# --- reaction-time metrics (Movement & Footwork) ----------------------------- #
# Only runs into a fast incoming ball where the player actually had to move.
REACT_INCOMING_KMH = 100.0   # incoming ball (previous shot) speed must exceed this (km/h)
REACT_MIN_MOVE_M = 1.5       # the run must cover at least this much path (m)
REACT_DIST_SHORT_M = 0.5     # report time to cover this distance (m)
REACT_DIST_LONG_M = 1.0      # report time to cover this distance (m)

FOOT_SCALE = 3.280839895   # m -> ft (m/s -> ft/s, m/s^2 -> ft/s^2). 1.0 = metric
SPEED_TO_MPH = 0.621371    # SPEED is km/h in this data -> mph. Set 1.0 if already mph

# --- serve attempt resolution ------------------------------------------------ #
NON_ATTEMPT_OUTCOMES = ("Let", "Extra")   # rallies that never consumed an attempt
DUPLICATE_BOUNCE_M = 0.3     # two serve rows landing within this (m) of each other...
DUPLICATE_SPEED = 10.0       # ...at this similar a speed, same placement = one serve
                             # (SPEED unit-agnostic: the gate is a loose sanity check)

PCT_DECIMALS = 1
SPEED_DECIMALS = 1
DIST_DECIMALS = 2
TIME_DECIMALS = 3          # reaction times are in seconds (0.02 s frame resolution)

# ============================ HELPERS ======================================= #


def _col(df, name):
    if name in df.columns:
        return df[name]
    return pd.Series(np.nan, index=df.index)


def _mean(series):
    s = pd.to_numeric(series, errors="coerce").dropna()
    return None if len(s) == 0 else float(s.mean())


def _speed_mph(series):
    v = _mean(series)
    return None if v is None else v * SPEED_TO_MPH


def _pct(numerator, denominator):
    if not denominator:
        return None
    return round(numerator / denominator * 100.0, PCT_DECIMALS)


def _round(value, ndigits):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    return round(float(value), ndigits)


def _to_float(v):
    """Coerce a scalar to float, returning NaN for None/blank/non-numeric."""
    try:
        return float(v)
    except (TypeError, ValueError):
        return float("nan")


def _time_to_distance(cum, dt, target):
    """Seconds from the start of a run until its cumulative path length `cum`
    (per-sample cumsum) first reaches `target` metres. NaN if never reached."""
    if cum.size == 0 or cum[-1] < target:
        return float("nan")
    return float((int(np.searchsorted(cum, target)) + 1) * dt)


def _depth_from_baseline(rebound_x):
    """Rally/return depth = distance to the baseline = REBOUND_X_abs - BASELINE_X
    (negative = short of the baseline, 0 = on it, positive = beyond it)."""
    v = _mean(rebound_x)
    return None if v is None else v - BASELINE_X


def _width_to_sideline(rebound_y):
    """Rally/return width = distance to the nearer sideline =
    |SIDELINE_Y - |REBOUND_Y_mirrored||."""
    s = pd.to_numeric(rebound_y, errors="coerce").dropna()
    if len(s) == 0:
        return None
    return float((SIDELINE_Y - s.abs()).abs().mean())


SERVE_BODY_LABELS = ("Body", "body", "B")   # serve_direction values treated as body serves


def _not_body(frame):
    """Mask of serves that are NOT body serves (body serves are excluded from
    accuracy since they are not aimed at a line). Keeps all rows if the
    serve_direction column is absent."""
    d = _col(frame, "serve_direction").astype(str)
    return ~d.isin([str(x) for x in SERVE_BODY_LABELS])


def metric(value, n):
    return {"value": value, "sample_size": int(n)}


NA = {"value": None, "sample_size": 0, "note": "not available from this data"}


def ratio_metric(num, den):
    """Ratio num/den of two win% metrics, carrying the components for context.
    >1 means the player over-performs the baseline (e.g. clutch on break points)."""
    nv = num.get("value") if isinstance(num, dict) else None
    dv = den.get("value") if isinstance(den, dict) else None
    val = None if (nv is None or not dv) else round(nv / dv, 3)
    return {"value": val, "numerator": nv, "denominator": dv,
            "numerator_n": (num or {}).get("sample_size"), "denominator_n": (den or {}).get("sample_size")}


def parse_track(s):
    """Parse a stringified numeric array (list-format or numpy-print format)."""
    if s is None or (isinstance(s, float) and math.isnan(s)):
        return None
    s = str(s).strip()
    if not s or s.lower() == "nan":
        return None
    try:
        return [float(x) for x in ast.literal_eval(s)]
    except (ValueError, SyntaxError):
        try:
            cleaned = s.replace("[", " ").replace("]", " ").replace("\n", " ")
            return [float(x) for x in cleaned.split()]
        except ValueError:
            return None


# ==================== SERVE ATTEMPT RESOLUTION ============================== #

# Column-name candidates: the adapted schema this script consumes first, the raw
# CV schema (pre-cv_adapter parquet dumps) second. Add names here if a pipeline
# labels them differently — resolution degrades gracefully when one is missing.
_C_SHOT = ("shot_no", "shot")
_C_ATTEMPT = ("serve_number", "serve")
_C_OUTCOME = ("outcome",)
_C_IS_IN = ("is_shot_in",)
_C_PLACEMENT = ("serve_direction", "placement_gsa", "placement")
_C_BOUNCE_X = ("REBOUND_X_abs", "bounce_x")
_C_BOUNCE_Y = ("REBOUND_Y_mirrored", "bounce_y")
_C_SPEED = ("SPEED", "speed")


def _pick(df, names):
    """First of `names` present in the frame, else None."""
    for n in names:
        if n in df.columns:
            return n
    return None


def _point_key(d):
    """Point identifier, whether or not the frame carries point_id."""
    if "point_id" in d.columns:
        return d["point_id"].astype(str)
    for cols in (("match_id", "set_no", "game_no", "point_no"),
                 ("match_id", "set", "game", "point")):
        present = [c for c in cols if c in d.columns]
        if len(present) >= 2:
            key = d[present[0]].astype(str)
            for c in present[1:]:
                key = key + "_" + d[c].astype(str)
            return key
    return pd.Series("0", index=d.index)


def resolve_serve_attempts(df, point_cols=None):
    """Drop the rallies that were never played and number the rest 1st / 2nd serve.

    A point is a run of rallies, each opened by a serve row (shot_no == 1). Three
    kinds of rally never happened and must not consume a service attempt:

      * lets and phantom detections (outcome 'Let' / 'Extra');
      * a rally whose serve duplicates a later one in the same point — same
        placement, same landing spot, same speed — i.e. the CV wrote the same
        rally down twice;
      * anything before the last two rallies, since a point holds at most two
        serves.

    Returns `df` without those rows, plus three columns, each carrying the value
    of the rally the row belongs to (so returns and +1 shots inherit them):

      rally_no       1-based rally index within the point
      serve_attempt  attempt number (1 or 2)
      serve_outcome  'in' / 'out' for that attempt

    The frame's own attempt column (`serve_number` / `serve`) is overwritten with
    the corrected number so existing key/group code keeps working. Idempotent:
    re-running on an already-resolved frame changes nothing.
    """
    d = df.reset_index(drop=True).copy()
    shot = _pick(d, _C_SHOT)
    attempt_col = _pick(d, _C_ATTEMPT)
    is_serve = (pd.to_numeric(d[shot], errors="coerce") == 1) if shot else None

    if is_serve is None or not bool(is_serve.any()):
        # No serve rows to anchor the numbering on (e.g. a rally-only frame):
        # leave the caller's numbering alone rather than zeroing it out.
        d["rally_no"] = (pd.to_numeric(d[attempt_col], errors="coerce")
                         if attempt_col else 1)
        d["serve_attempt"] = d["rally_no"]
        d["serve_outcome"] = "in"
        return d

    drop_key = None
    if point_cols is None:
        d["_pt_key"] = _point_key(d)
        point_cols, drop_key = ["_pt_key"], "_pt_key"
    pt = d.groupby(point_cols, sort=False).ngroup()
    rally = is_serve.astype(int).groupby(pt).cumsum()

    oc = _pick(d, _C_OUTCOME)
    outcome = d[oc].astype(object) if oc else pd.Series(index=d.index, dtype=object)

    # 1. lets / phantom rallies: drop the whole rally its serve row opened
    junk = is_serve & outcome.isin(NON_ATTEMPT_OUTCOMES)
    drop = junk.groupby([pt, rally]).transform("max").astype(bool)

    # 2. duplicated serve rows, and anything before the last two attempts
    place = _pick(d, _C_PLACEMENT)
    bx, by, sp = _pick(d, _C_BOUNCE_X), _pick(d, _C_BOUNCE_Y), _pick(d, _C_SPEED)
    can_compare = all(c is not None for c in (place, bx, by, sp))
    if can_compare:
        x = pd.to_numeric(d[bx], errors="coerce")
        y = pd.to_numeric(d[by], errors="coerce")
        v = pd.to_numeric(d[sp], errors="coerce")

    dead = set()
    srv_idx = d.index[is_serve & ~drop]
    for _, idx in pd.Series(srv_idx).groupby(pt[srv_idx].values, sort=False):
        rallies = [(i, rally[i]) for i in idx]
        for (i, ri), (j, _) in zip(rallies, rallies[1:]):
            same_serve = can_compare and (
                d.at[i, place] == d.at[j, place]
                and pd.notna(x[i]) and pd.notna(x[j]) and abs(x[i] - x[j]) < DUPLICATE_BOUNCE_M
                and pd.notna(y[i]) and pd.notna(y[j]) and abs(y[i] - y[j]) < DUPLICATE_BOUNCE_M
                and pd.notna(v[i]) and pd.notna(v[j]) and abs(v[i] - v[j]) < DUPLICATE_SPEED
            )
            if same_serve:
                dead.add((pt[i], ri))       # the earlier of the pair is the copy
        # a point cannot hold more than two attempts — keep the last two
        alive = [(pt[i], ri) for i, ri in rallies if (pt[i], ri) not in dead]
        for key in alive[:-2]:
            dead.add(key)
    if dead:
        drop = drop | pd.Series(list(zip(pt, rally)), index=d.index).isin(dead)

    d = d[~drop].copy()
    pt, is_serve = pt[~drop], is_serve[~drop]
    rally_no = is_serve.astype(int).groupby(pt).cumsum()      # renumbered, contiguous
    attempt = rally_no.clip(upper=2)

    # in/out from the point structure: an attempt with another behind it was out;
    # the last attempt was in unless the point ended on a fault (double fault).
    played = attempt.groupby(pt).transform("max")
    if oc:
        faulted = d[oc].astype(object).eq("Fault")
    elif _pick(d, _C_IS_IN):
        faulted = pd.to_numeric(d[_pick(d, _C_IS_IN)], errors="coerce").eq(0)
    else:
        faulted = pd.Series(False, index=d.index)
    out = (attempt < played) | (is_serve & faulted)
    out = out.groupby([pt, attempt]).transform("max").astype(bool)

    d["rally_no"] = rally_no
    d["serve_attempt"] = attempt
    d["serve_outcome"] = np.where(out, "out", "in")
    for name in _C_ATTEMPT:                 # keep the frame's own column in sync
        if name in d.columns:
            d[name] = attempt
    if drop_key:
        d = d.drop(columns=[drop_key])
    return d.reset_index(drop=True)


# ============================ METRIC ENGINE ================================= #


class MatchMetrics:
    """Every metric is computed from the point of view of `player`."""

    SORT_KEYS = ["match_id", "set_no", "game_no", "point_no", "rally_no",
                 "serve_number", "shot_no"]

    def __init__(self, player, serves_df, movement_df):
        self.player = player

        # Resolve service attempts FIRST: rallies that were never played are
        # dropped and serve_attempt / serve_outcome / rally_no are attached to
        # every row, so nothing downstream reads the raw serve_number. No-op on
        # frames that were already resolved.
        same_frame = movement_df is serves_df
        serves_df = resolve_serve_attempts(serves_df)
        movement_df = serves_df if same_frame else resolve_serve_attempts(movement_df)

        # serves_df: every serve/return event across all points (no tracking).
        # Used for serve, return, +1 win, pressure, and overall-win metrics.
        self.sdf = serves_df.reset_index(drop=True)

        # movement_df: rally shots for points with COMPLETE movement tracking.
        # Used for forehand/backhand, net, rally, movement, and court position.
        # Sort chronologically so "the previous shot" is well defined.
        keys = [k for k in self.SORT_KEYS if k in movement_df.columns]
        self.mdf = (movement_df.sort_values(keys).reset_index(drop=True)
                    if keys else movement_df.reset_index(drop=True))

        # Point winner: PLAYER_WIN_NAME is blank on some rows (e.g. the serve
        # row), so take the first non-null winner per point. serves_df covers all
        # points, so use it as the authoritative winner map for every win% metric.
        wb = (self.sdf.dropna(subset=["PLAYER_WIN_NAME"])
              .groupby("point_id")["PLAYER_WIN_NAME"].first())
        self._winner = wb.to_dict()

        # The distance-moved columns (and the matching location track) describe
        # movement AFTER the shot. So the movement INTO a shot is the previous
        # shot's value within the same point. Built on movement_df.
        self._key_to_idx = {}
        for idx, row in self.mdf.iterrows():
            self._key_to_idx[(row.get("point_id"), row.get("serve_number"), row.get("shot_no"))] = idx
        # Hawk-Eye has per-frame tracking arrays (server/returner_location_*); CV
        # has one location per shot (player_location_*) + time_passed. Detect and
        # set up movement accordingly (CV movement is per-shot, Start-End only).
        self._is_cv = ("player_location_x" in self.mdf.columns
                       and "server_location_x" not in self.mdf.columns)
        if self._is_cv:
            self._setup_cv_movement()
        else:
            player_dist = self._player_distance_moved(self.mdf)          # after-shot, per row
            dist_into = pd.Series(np.nan, index=self.mdf.index)
            prev_rebound = pd.Series(np.nan, index=self.mdf.index)       # incoming ball's rebound x
            reb = pd.to_numeric(_col(self.mdf, "REBOUND_X_abs"), errors="coerce")
            for idx, row in self.mdf.iterrows():
                prev = self._key_to_idx.get((row.get("point_id"), row.get("serve_number"), row.get("shot_no") - 1))
                if prev is not None:
                    dist_into.at[idx] = player_dist.at[prev]
                    prev_rebound.at[idx] = reb.at[prev]
            self._dist_into = dist_into                                  # movement to REACH each shot
            # is_volley: the incoming ball did not bounce (its rebound x equals this
            # shot's contact x, to 2 dp) and contact is inside the net zone.
            contact = pd.to_numeric(_col(self.mdf, "CONTACT_X_abs"), errors="coerce")
            self._is_volley = ((prev_rebound.round(2) == contact.round(2))
                               & (contact < VOLLEY_CONTACT_X_MAX))

        # displacement state for the manual-pipeline movement block (below)
        self._setup_manual_movement()

    def _prev_row(self, row):
        prev = self._key_to_idx.get((row.get("point_id"), row.get("serve_number"), row.get("shot_no") - 1))
        return None if prev is None else self.mdf.iloc[prev]

    def _setup_cv_movement(self):
        """CV movement: one location per shot. THIS player's location is
        player_location_* when hitting and receiver_location_* when receiving; the
        displacement from the previous shot (within the rally) is the movement to
        REACH each shot, over time_passed. Only Start-End quantities exist here."""
        d = self.mdf
        hit = d.PLAYER_HIT == self.player
        px = pd.to_numeric(pd.Series(np.where(hit, _col(d, "player_location_x"),
                                              _col(d, "receiver_location_x")), index=d.index), errors="coerce")
        py = pd.to_numeric(pd.Series(np.where(hit, _col(d, "player_location_y"),
                                              _col(d, "receiver_location_y")), index=d.index), errors="coerce")
        pym = pd.Series(np.where(px < 0, py, -py), index=d.index)     # mirrored: <0 deuce, >0 ad
        keys = [d[c] for c in ("point_id", "serve_number") if c in d.columns] or [pd.Series(0, index=d.index)]
        px_prev = px.groupby(keys).shift(1)
        pym_prev = pym.groupby(keys).shift(1)
        self._cv_t = pd.to_numeric(_col(d, "time_passed"), errors="coerce")
        self._cv_dx = px.abs() - px_prev.abs()          # longitudinal (toward/away from net)
        self._cv_dy = pym - pym_prev                     # lateral, mirrored
        self._cv_dist = np.sqrt(self._cv_dx ** 2 + self._cv_dy ** 2)
        self._cv_net = px_prev.abs() - px.abs()          # >0 = moved toward the net
        self._dist_into = self._cv_dist                  # movement to REACH each shot
        ev = _col(d, "events.shot").astype(str).str.lower()
        self._is_volley = ev.str.contains("volley", na=False)

    def _setup_manual_movement(self):
        """Per-shot displacement state, copied from the manual pipeline
        (utr_match_metrics_manual5newspeed_all.CvShotMetrics.__init__), feeding
        movement_block() below.

            player_x   = hitter -> player_location_x, else receiver_location_x
                         (tracks THIS player on every shot of the rally)
            *_previous = shift(1) within the rally
            y mirrored by side; x uses abs()
            speed = dist / t * ft ;  acceleration = dist / t**2 * ft

        Only the group keys differ from the manual script: the rally key falls
        back to this schema's set_no/game_no/point_no/serve_number names before
        the manual script's set/game/point/serve, then to rally_id / point_id."""
        d = self.mdf
        hit = d.PLAYER_HIT == self.player
        px = pd.to_numeric(pd.Series(np.where(hit, _col(d, "player_location_x"),
                                              _col(d, "receiver_location_x")), index=d.index), errors="coerce")
        py = pd.to_numeric(pd.Series(np.where(hit, _col(d, "player_location_y"),
                                              _col(d, "receiver_location_y")), index=d.index), errors="coerce")
        py_m = pd.Series(np.where(px < 0, py, -py), index=d.index)
        gcols = [c for c in ("match_id", "set_no", "game_no", "point_no", "serve_number") if c in d.columns]
        if len(gcols) < 3:
            gcols = [c for c in ("match_id", "set", "game", "point", "serve") if c in d.columns]
        g = (d[gcols].astype(str).agg("|".join, axis=1) if len(gcols) >= 3
             else (d["rally_id"] if "rally_id" in d.columns else _col(d, "point_id")))
        px_prev = px.groupby(g).shift(1)
        pym_prev = py_m.groupby(g).shift(1)
        t = pd.to_numeric(_col(d, "time_passed"), errors="coerce")
        dx = px.abs() - px_prev.abs()          # longitudinal (x), signed
        dy = py_m - pym_prev                   # lateral (y), signed
        self._dist = np.sqrt(dx ** 2 + dy ** 2)
        self._time = t
        with np.errstate(divide="ignore", invalid="ignore"):
            self._speed = self._dist / t * FOOT_SCALE
            self._accel = self._dist / t ** 2 * FOOT_SCALE
            self._lon_speed = dx.abs() / t * FOOT_SCALE
            self._lat_speed = dy.abs() / t * FOOT_SCALE
            self._lon_acc = dx.abs() / t ** 2 * FOOT_SCALE
            self._lat_acc = dy.abs() / t ** 2 * FOOT_SCALE
        self._has_movement = bool(self._dist.notna().any())

    def _win_pct_over_points(self, point_id_series):
        pts = pd.unique(point_id_series)
        wins = sum(1 for p in pts if self._winner.get(p) == self.player)
        return metric(_pct(wins, len(pts)), len(pts))

    # ---- selectors --------------------------------------------------------- #

    def _serves(self, sn, in_only=False):
        """One row per service ATTEMPT of number `sn` hit by the player.

        Populations come from the resolved serve_attempt / serve_outcome, never
        from (serve_number == sn) & is_shot_in — the raw numbering over-counts
        attempts whenever a let, a phantom 'Extra' detection or a duplicated CV
        serve row sits in the point, which inflates the 1st Serve In% denominator
        and leaks genuine 1st serves into the 2nd-serve population."""
        d = self.sdf
        mask = (d.PLAYER_HIT == self.player) & (d.shot_no == 1) & (d.serve_attempt == sn)
        if in_only:
            mask &= d.serve_outcome == "in"
        return d[mask]

    def _returns(self, sn, in_only=False):
        """The player's return rows off an IN serve of attempt number `sn`.

        serve_attempt is carried by every row of the rally, so the return is
        matched to the attempt that actually opened it; `in_only` still refers to
        the return's own landing (is_shot_in), not to the serve's."""
        d = self.sdf
        mask = ((d.PLAYER_HIT == self.player) & (d.shot_no == 2)
                & (d.serve_attempt == sn) & (d.serve_outcome == "in"))
        if in_only:
            mask &= d.is_shot_in == 1
        return d[mask]

    def _rally_all(self, shot_type=None):
        d = self.mdf
        mask = (d.PLAYER_HIT == self.player) & (d.shot_no >= RALLY_MIN_SHOT_NO)
        if shot_type is not None:
            mask &= d.shot_type == shot_type
        return d[mask]

    def _rally_in(self, shot_type=None):
        r = self._rally_all(shot_type)
        return r[r.is_shot_in == 1]

    def _player_distance_moved(self, frame):
        is_srv = frame.server_name == self.player
        srv = pd.to_numeric(_col(frame, "server_shot_distance_moved"), errors="coerce")
        ret = pd.to_numeric(_col(frame, "returner_shot_distance_moved"), errors="coerce")
        return srv.where(is_srv, ret)

    def _running_mask(self, frame):
        # movement to REACH the shot = previous shot's distance moved
        return self._dist_into.loc[frame.index] > RUNNING_DISTANCE_M

    def _player_track(self, row):
        if row.server_name == self.player:
            return parse_track(row.get("server_location_x")), parse_track(row.get("server_location_y"))
        return parse_track(row.get("returner_location_x")), parse_track(row.get("returner_location_y"))

    def _opponent_track(self, row):
        if row.server_name == self.player:
            return parse_track(row.get("returner_location_x")), parse_track(row.get("returner_location_y"))
        return parse_track(row.get("server_location_x")), parse_track(row.get("server_location_y"))

    # ===================== SERVE ===================== #

    def serve_in_pct(self, sn):
        a = self._serves(sn)
        return metric(_pct((a.serve_outcome == "in").sum(), len(a)), len(a))

    def serve_speed(self, sn, side=None, direction=None):
        s = self._serves(sn, in_only=True)
        if side is not None:
            s = s[s.serve_deuce_or_ad == side]
        if direction is not None:
            s = s[s.serve_direction == direction]
        return metric(_round(_speed_mph(s.SPEED), SPEED_DECIMALS), len(s))

    def serve_accuracy(self, sn, side=None):
        s = self._serves(sn, in_only=True)
        if side is not None:
            s = s[s.serve_deuce_or_ad == side]
        s = s[_not_body(s)]   # body serves are not aimed at a line -> excluded
        return metric(_round(_mean(_col(s, "distance_from_side_or_center_line")), DIST_DECIMALS), len(s))

    def serve_plus1_win(self, sn):
        d = self.sdf
        p = d[(d.shot_no == 3) & (d.PLAYER_HIT == self.player)
              & (d.serve_attempt == sn) & (d.serve_outcome == "in")
              & (d.server_name == self.player)]
        return self._win_pct_over_points(p.point_id)

    # ===================== RETURN ===================== #

    def return_speed(self, sn):
        r = self._returns(sn, in_only=True)
        return metric(_round(_speed_mph(r.SPEED), SPEED_DECIMALS), len(r))

    def return_in_pct(self, sn):
        a = self._returns(sn)
        return metric(_pct((a.is_shot_in == 1).sum(), len(a)), len(a))

    def return_depth(self, sn):
        r = self._returns(sn, in_only=True)
        return metric(_round(_depth_from_baseline(_col(r, "REBOUND_X_abs")), DIST_DECIMALS), len(r))

    def return_width(self, sn):
        r = self._returns(sn, in_only=True)
        return metric(_round(_width_to_sideline(_col(r, "REBOUND_Y_mirrored")), DIST_DECIMALS), len(r))

    def return_plus1_win(self, sn):
        d = self.sdf
        p = d[(d.shot_no == 4) & (d.PLAYER_HIT == self.player)
              & (d.serve_attempt == sn) & (d.serve_outcome == "in")
              & (d.server_name != self.player)]
        return self._win_pct_over_points(p.point_id)

    def return_win(self, sn):
        """Baseline win% on every return point facing an IN serve of that number.
        Denominator for the +1 ratios (manual pipeline's DataRallyMetrics.return_win);
        not reported on its own, same as in the manual script."""
        return self._win_pct_over_points(self._returns(sn).point_id)

    # ===================== FOREHAND / BACKHAND ===================== #

    def stroke_speed(self, shot_type, side=None):
        r = self._rally_in(shot_type)
        if side == "deuce":
            r = r[_col(r, "CONTACT_Y_mirrored") < DEUCE_SIDE_Y]
        elif side == "ad":
            r = r[_col(r, "CONTACT_Y_mirrored") > AD_SIDE_Y]
        return metric(_round(_speed_mph(r.SPEED), SPEED_DECIMALS), len(r))

    def stroke_in_pct(self, shot_type, side=None):
        r = self._rally_all(shot_type)
        if side == "deuce":
            r = r[_col(r, "CONTACT_Y_mirrored") < DEUCE_SIDE_Y]
        elif side == "ad":
            r = r[_col(r, "CONTACT_Y_mirrored") > AD_SIDE_Y]
        return metric(_pct((r.is_shot_in == 1).sum(), len(r)), len(r))

    def bh_in_pct_movement(self, running):
        r = self._rally_all("B")
        run = self._running_mask(r)
        r = r[run] if running else r[~run]
        return metric(_pct((r.is_shot_in == 1).sum(), len(r)), len(r))

    # ===================== NET ===================== #

    def volley_win_pct(self):
        d = self.mdf
        v = d[(d.PLAYER_HIT == self.player) & (d.shot_no >= RALLY_MIN_SHOT_NO)
              & self._is_volley]
        return self._win_pct_over_points(v.point_id)

    # ===================== RALLY ===================== #

    def rally_width(self, movement=None):
        r = self._rally_in()
        if movement == "running":
            r = r[self._running_mask(r)]
        elif movement == "stationary":
            r = r[~self._running_mask(r)]
        return metric(_round(_width_to_sideline(_col(r, "REBOUND_Y_mirrored")), DIST_DECIMALS), len(r))

    def rally_depth(self):
        r = self._rally_in()
        return metric(_round(_depth_from_baseline(_col(r, "REBOUND_X_abs")), DIST_DECIMALS), len(r))

    # ===================== MOVEMENT & FOOTWORK ===================== #

    def _gather_runs(self):
        """One run = the player's movement to REACH a ball they hit. Because the
        location track / distance-moved on a row describe movement AFTER that
        shot, the run leading into the player's shot is the PREVIOUS shot's
        window (the opponent's shot, same point), where the player's own track
        is the path from the opponent's contact to the player reaching the ball.
        Three speed/acceleration definitions are precomputed per run on the foot
        (magnitude), longitudinal (x) and lateral (y) axes.
        """
        if self._is_cv:
            return self._gather_runs_cv()
        own = self.mdf[(self.mdf.PLAYER_HIT == self.player)
                       & (self.mdf.shot_no >= RALLY_MIN_SHOT_NO)]
        runs = []
        for idx, row in own.iterrows():
            prev = self._prev_row(row)
            if prev is None:
                continue
            xs, ys = self._player_track(prev)            # player's path to reach this ball
            if xs is None or ys is None:
                continue
            n = min(len(xs), len(ys))
            if n < 3:
                continue
            x = np.asarray(xs[:n], dtype=float)
            y = np.asarray(ys[:n], dtype=float)
            dt = FRAME_DT
            dx, dy = np.diff(x), np.diff(y)
            sp = np.sqrt(dx ** 2 + dy ** 2) / dt          # instantaneous foot speed
            lon = np.abs(dx) / dt                          # Hawk-Eye X = longitudinal
            lat = np.abs(dy) / dt                          # Hawk-Eye Y = lateral
            t = (n - 1) * dt                               # elapsed time of the run
            mv = self._dist_into.at[idx]                   # distance moved to reach this shot

            # context for the directional run categories (incoming ball + path).
            # lat_mir folds Y to the mirrored frame (flip when contacted from +X)
            # so <0 is deuce/right and >0 is ad/left; net_disp>0 = moved netward.
            net_disp = abs(float(x[0])) - abs(float(x[-1]))
            lat_mir = (float(y[-1]) - float(y[0])) * (-1.0 if x[-1] > 0 else 1.0)
            # reaction-time context: cumulative path along the run (t=0 is the
            # start of the run window ~ the incoming-ball contact), the time to
            # cover fixed distances, and the time to reach peak instantaneous speed.
            step = np.hypot(dx, dy)
            cum = np.cumsum(step)
            ctx = {
                "lat_mir": lat_mir,
                "net_disp": net_disp,
                "prev_speed": _to_float(prev.get("SPEED")),          # incoming ball speed (km/h)
                "prev_rebound_x": _to_float(prev.get("REBOUND_X_abs")),
                "prev_spin": _to_float(prev.get("spinRPM")),
                "prev_is_drop": bool(_to_float(prev.get("spinRPM")) < 0),   # backspin = dropshot
                "path_total": float(cum[-1]) if cum.size else 0.0,   # cumulative metres in the run
                "t_peak": float((int(np.argmax(sp)) + 1) * dt) if sp.size else float("nan"),
                "t_move_05": _time_to_distance(cum, dt, REACT_DIST_SHORT_M),
                "t_move_10": _time_to_distance(cum, dt, REACT_DIST_LONG_M),
            }

            run = {
                "ran": bool(mv > RUNNING_DISTANCE_M) if mv == mv else False,
                "ctx": ctx,
                "speed": {
                    "foot": {"se": math.hypot(x[-1] - x[0], y[-1] - y[0]) / t,
                             "max": float(sp.max()), "avg": float(sp.mean())},
                    "lon": {"se": abs(x[-1] - x[0]) / t,
                            "max": float(lon.max()), "avg": float(lon.mean())},
                    "lat": {"se": abs(y[-1] - y[0]) / t,
                            "max": float(lat.max()), "avg": float(lat.mean())},
                },
                "accel": None,
            }
            if len(sp) >= 2:                               # need >=2 speed samples
                acc = np.diff(sp) / dt
                lon_a = np.diff(lon) / dt
                lat_a = np.diff(lat) / dt
                ta = (len(sp) - 1) * dt
                run["accel"] = {
                    "foot": {"se": abs(sp[-1] - sp[0]) / ta,
                             "max": float(np.abs(acc).max()), "avg": float(np.abs(acc).mean())},
                    "lon": {"se": abs(lon[-1] - lon[0]) / ta,
                            "max": float(np.abs(lon_a).max()), "avg": float(np.abs(lon_a).mean())},
                    "lat": {"se": abs(lat[-1] - lat[0]) / ta,
                            "max": float(np.abs(lat_a).max()), "avg": float(np.abs(lat_a).mean())},
                }
            runs.append(run)
        return runs

    def _gather_runs_cv(self):
        """CV runs: one per player rally shot, from the per-shot displacement to
        reach it (see _setup_cv_movement). Only Start-End ('se') quantities exist;
        Max / per-sample Average and the reaction times need per-frame data -> NaN.
        Dropshot is taken from events.shot == 'dropshot' on the incoming ball."""
        own = self.mdf[(self.mdf.PLAYER_HIT == self.player)
                       & (self.mdf.shot_no >= RALLY_MIN_SHOT_NO)]
        ev = _col(self.mdf, "events.shot").astype(str).str.lower()
        has_spin = "spinRPM" in self.mdf.columns
        nan = float("nan")
        runs = []
        for idx, row in own.iterrows():
            prev = self._prev_row(row)
            if prev is None:
                continue
            dist = self._cv_dist.at[idx]
            t = self._cv_t.at[idx]
            dx, dy = self._cv_dx.at[idx], self._cv_dy.at[idx]
            if not (dist == dist) or not (t == t) or t <= 0:
                continue
            prev_idx = self._key_to_idx.get((row.get("point_id"), row.get("serve_number"),
                                             row.get("shot_no") - 1))
            prev_is_drop = "dropshot" in str(ev.at[prev_idx]) if prev_idx is not None else False
            if has_spin:
                prev_is_drop = prev_is_drop or (_to_float(prev.get("spinRPM")) < 0)
            runs.append({
                "ran": bool(dist > RUNNING_DISTANCE_M),
                "ctx": {
                    "lat_mir": float(dy),
                    "net_disp": float(self._cv_net.at[idx]),
                    "prev_speed": _to_float(prev.get("SPEED")),
                    "prev_rebound_x": _to_float(prev.get("REBOUND_X_abs")),
                    "prev_spin": _to_float(prev.get("spinRPM")) if has_spin else nan,
                    "prev_is_drop": bool(prev_is_drop),
                    "path_total": float(dist),
                    "t_peak": nan, "t_move_05": nan, "t_move_10": nan,   # no per-frame data
                },
                "speed": {
                    "foot": {"se": dist / t, "max": nan, "avg": nan},
                    "lon": {"se": abs(dx) / t, "max": nan, "avg": nan},
                    "lat": {"se": abs(dy) / t, "max": nan, "avg": nan},
                },
                "accel": {
                    "foot": {"se": dist / t ** 2, "max": nan, "avg": nan},
                    "lon": {"se": abs(dx) / t ** 2, "max": nan, "avg": nan},
                    "lat": {"se": abs(dy) / t ** 2, "max": nan, "avg": nan},
                },
            })
        return runs

    @staticmethod
    def _agg_runs(runs, kind, axis, approach):
        """Aggregate one per-run quantity across runs as the median and the 95th
        percentile (both scaled m->ft). Null stats with sample_size 0 if empty."""
        vals = [r[kind][axis][approach] for r in runs
                if r.get(kind) is not None and r[kind][axis][approach] == r[kind][axis][approach]]
        if not vals:
            return {"median": None, "p95": None, "sample_size": 0}
        arr = np.asarray(vals, dtype=float) * FOOT_SCALE
        return {
            "median": _round(float(np.median(arr)), SPEED_DECIMALS),
            "p95": _round(float(np.percentile(arr, 95)), SPEED_DECIMALS),
            "sample_size": int(len(vals)),
        }

    @staticmethod
    def _agg_times(runs, key):
        """Aggregate one per-run reaction time (seconds, NOT foot-scaled) across
        runs as the median and the 5th percentile (the fastest reactions)."""
        vals = [r["ctx"][key] for r in runs
                if r.get("ctx") is not None and r["ctx"].get(key) == r["ctx"].get(key)]
        if not vals:
            return {"median": None, "p05": None, "sample_size": 0}
        arr = np.asarray(vals, dtype=float)
        return {
            "median": _round(float(np.median(arr)), TIME_DECIMALS),
            "p05": _round(float(np.percentile(arr, 5)), TIME_DECIMALS),
            "sample_size": int(len(vals)),
        }

    def _three_approaches(self, runs, kind, axis):
        return {
            "Start-End": self._agg_runs(runs, kind, axis, "se"),
            "Max": self._agg_runs(runs, kind, axis, "max"),
            "Average": self._agg_runs(runs, kind, axis, "avg"),
        }

    # ---- movement block, copied from utr_match_metrics_manual5newspeed_all --- #
    # (the _gather_runs* / _agg_runs / _agg_times / _three_approaches helpers
    #  above are now unused; kept in place so the swap is easy to revert.)

    # per-frame movement columns attached by cv_to_json_df (players_positions)
    MOVE_FRAME_COLS = ("move_spd_avg", "move_spd_max", "move_spd_min", "move_spd_se",
                       "move_acc_max", "move_dec_max",
                       "move_lon_avg", "move_lon_max", "move_lon_min", "move_lon_acc_max", "move_lon_dec_max",
                       "move_lat_avg", "move_lat_max", "move_lat_min", "move_lat_acc_max", "move_lat_dec_max")

    def movement_block(self):
        """Per-frame movement from the CV players_positions track when available
        (move_* columns), else the displacement-only fallback."""
        if any(c in self.mdf.columns for c in self.MOVE_FRAME_COLS):
            return self._movement_block_frames()
        return self._movement_block_displacement()

    def _movement_block_frames(self):
        """Foot / longitudinal / lateral speed (avg, max, min, start-end) plus
        proper acceleration (Max) and deceleration (Min, i.e. hardest braking, a
        negative value), from the per-frame player track over the run to REACH
        each rally shot (opponent hit -> player reaches ball). Mean across the
        player's rally runs (shot >= RALLY_MIN_SHOT_NO, in), m->ft."""
        d = self.mdf
        r = d[(d.PLAYER_HIT == self.player) & (d.shot_no >= RALLY_MIN_SHOT_NO) & (d.is_shot_in == 1)]

        def agg(col, negate=False):
            """Aggregate a per-run column across the player's runs (m->ft): mean
            (value), median, 95th percentile, sample size. `negate` flips the sign
            so deceleration reads as a positive magnitude — its hard-braking
            extreme is then the 95th percentile, like every other metric."""
            s = pd.to_numeric(_col(r, col), errors="coerce").dropna()
            if not len(s):
                return {"value": None, "median": None, "p95": None, "sample_size": 0}
            arr = s.to_numpy(dtype=float) * FOOT_SCALE
            if negate:
                arr = -arr
            return {"value": _round(float(arr.mean()), SPEED_DECIMALS),
                    "median": _round(float(np.median(arr)), SPEED_DECIMALS),
                    "p95": _round(float(np.percentile(arr, 95)), SPEED_DECIMALS),
                    "sample_size": int(len(arr))}

        return {
            "Foot Speed [ft/s]": {"Average": agg("move_spd_avg"), "Max": agg("move_spd_max"),
                                  "Min": agg("move_spd_min"), "Start-End": agg("move_spd_se")},
            "Foot Acceleration [ft/s²]": agg("move_acc_max"),
            "Foot Deceleration [ft/s²]": agg("move_dec_max", negate=True),
            "Longitudinal Speed [ft/s]": {"Average": agg("move_lon_avg"), "Max": agg("move_lon_max"),
                                          "Min": agg("move_lon_min")},
            "Longitudinal Acceleration [ft/s²]": agg("move_lon_acc_max"),
            "Longitudinal Deceleration [ft/s²]": agg("move_lon_dec_max", negate=True),
            "Lateral Speed [ft/s]": {"Average": agg("move_lat_avg"), "Max": agg("move_lat_max"),
                                     "Min": agg("move_lat_min")},
            "Lateral Acceleration [ft/s²]": agg("move_lat_acc_max"),
            "Lateral Deceleration [ft/s²]": agg("move_lat_dec_max", negate=True),
        }

    def _movement_block_displacement(self):
        """Foot speed and acceleration per the manual pipeline's get_speed /
        get_acceleration: per-shot displacement / time (speed) and / time**2
        (acceleration), m->ft, over the player's groundstrokes from shot >= 3.
        Reported under Start-End (displacement-based); Max / per-sample Average
        need per-frame tracking -> null."""
        na3 = lambda: {"Start-End": NA, "Max": NA, "Average": NA}
        keys = ("Average Foot Speed [ft/s]", "Average Foot Acceleration [ft/s\u00b2]",
                "Avg. Lateral Speed in Rallies", "Average Longitudinal Speed in Rallies",
                "Average Lateral Acceleration in Rallies", "Average Longitudinal Acceleration in Rallies")
        if not self._has_movement or not self._time.notna().any():
            return {k: na3() for k in keys}

        d = self.mdf
        # player's groundstrokes that landed in, from shot >= 3 (matches get_speed)
        m = ((d.PLAYER_HIT == self.player) & (d.shot_no >= 3)
             & (d.shot_type.isin(["F", "B"])) & (d.is_shot_in == 1))
        idx = d[m].index
        run = self._dist[idx] > RUNNING_DISTANCE_M     # running subset for lateral/longitudinal

        def avg(series, mask=None):
            s = series[idx]
            if mask is not None:
                s = s[mask]
            s = s.replace([np.inf, -np.inf], np.nan).dropna()
            if not len(s):
                return NA
            # zeros are NOT dropped here: a 0 displacement means the player
            # genuinely did not move, unlike a 0 in a measured ball speed.
            return {"value": _round(float(s.mean()), SPEED_DECIMALS),
                    "mean": _round(float(s.mean()), SPEED_DECIMALS),
                    "median": _round(float(s.median()), SPEED_DECIMALS),
                    "sample_size": int(len(s))}

        return {
            "Average Foot Speed [ft/s]": {"Start-End": avg(self._speed), "Max": NA, "Average": NA},
            "Average Foot Acceleration [ft/s\u00b2]": {"Start-End": avg(self._accel), "Max": NA, "Average": NA},
            "Avg. Lateral Speed in Rallies": {"Start-End": avg(self._lat_speed, run), "Max": NA, "Average": NA},
            "Average Longitudinal Speed in Rallies": {"Start-End": avg(self._lon_speed, run), "Max": NA, "Average": NA},
            "Average Lateral Acceleration in Rallies": {"Start-End": avg(self._lat_acc, run), "Max": NA, "Average": NA},
            "Average Longitudinal Acceleration in Rallies": {"Start-End": avg(self._lon_acc, run), "Max": NA, "Average": NA},
        }

    # ===================== COURT POSITION ===================== #

    def player_distance_from_baseline(self):
        r = self._rally_in()
        val = _mean(_col(r, "CONTACT_X_abs"))
        val = None if val is None else _round(val - BASELINE_X, DIST_DECIMALS)
        return metric(val, len(r))

    def opponent_distance_from_baseline(self):
        if self._is_cv:
            # CV has no tracking; use the opponent's own contact depth on their
            # rally shots (matches manual4's CvShotMetrics).
            r = self.mdf[(self.mdf.PLAYER_HIT != self.player) & (self.mdf.shot_no >= RALLY_MIN_SHOT_NO)
                         & (self.mdf.is_shot_in == 1)]
            v = _mean(_col(r, "CONTACT_X_abs"))
            return metric(None if v is None else _round(v - BASELINE_X, DIST_DECIMALS), len(r))
        # opponent's tracked position at the player's contact (end of the run
        # window = previous shot's after-movement), on the player's own rally shots
        rows = self.mdf[(self.mdf.PLAYER_HIT == self.player) & (self.mdf.shot_no >= RALLY_MIN_SHOT_NO)
                        & (self.mdf.is_shot_in == 1)]
        vals = []
        for _, row in rows.iterrows():
            prev = self._prev_row(row)
            if prev is None:
                continue
            xs, _ys = self._opponent_track(prev)
            if xs:
                vals.append(abs(xs[-1]) - BASELINE_X)
        val = None if not vals else _round(float(np.mean(vals)), DIST_DECIMALS)
        return metric(val, len(vals))

    # ===================== PRESSURE / OVERALL ===================== #

    def _point_win_pct(self, mask):
        return self._win_pct_over_points(self.sdf[mask].point_id)

    def break_point_faced(self):
        d = self.sdf
        return self._point_win_pct((d.is_break_point == 1) & (d.server_name == self.player))

    def break_point_opportunity(self):
        d = self.sdf
        return self._point_win_pct((d.is_break_point == 1) & (d.server_name != self.player))

    def pressure_point_faced(self):
        d = self.sdf
        return self._point_win_pct((d.is_pressure_point == 1) & (d.server_name == self.player))

    def pressure_point_opportunity(self):
        d = self.sdf
        return self._point_win_pct((d.is_pressure_point == 1) & (d.server_name != self.player))

    def overall_serve_win(self):
        d = self.sdf
        return self._point_win_pct(d.server_name == self.player)

    def overall_return_win(self):
        d = self.sdf
        return self._point_win_pct(d.server_name != self.player)

    # ---------------------------------------------------------------- #

    def compute(self):
        return {
            "1st Serve": {
                "1st Serve In%": self.serve_in_pct(1),
                "1st Serve Speed": self.serve_speed(1),
                "1st Serve Deuce Wide Speed": self.serve_speed(1, "deuce", "W"),
                "1st Serve Deuce T Speed": self.serve_speed(1, "deuce", "T"),
                "1st Serve Ad Speed": self.serve_speed(1, "ad"),
                "1st Serve Accuracy [in meters]": self.serve_accuracy(1),
                "1st Serve Deuce Accuracy": self.serve_accuracy(1, "deuce"),
                "1st Serve Ad Accuracy": self.serve_accuracy(1, "ad"),
                "1st Serve +1 Win%": self.serve_plus1_win(1),
            },
            "2nd Serve": {
                "2nd Serve In%": self.serve_in_pct(2),
                "2nd Serve Speed": self.serve_speed(2),
                "2nd Serve Accuracy [in meters]": self.serve_accuracy(2),
                "2nd Serve +1 Win%": self.serve_plus1_win(2),
            },
            "Return": {
                "1st Serve Return Speed": self.return_speed(1),
                "1st Return In%": self.return_in_pct(1),
                "1st Return Depth (in meters)": self.return_depth(1),
                "1st Return Width (in meters)": self.return_width(1),
                "1st Serve Return +1 Win%": self.return_plus1_win(1),
                "2nd Serve Return Speed": self.return_speed(2),
                "2nd Return In%": self.return_in_pct(2),
                "2nd Return Depth (in meters)": self.return_depth(2),
                "2nd Return Width (in meters)": self.return_width(2),
                "2nd Serve Return +1 Win%": self.return_plus1_win(2),
            },
            "Forehand": {
                "Deuce FH Speed [MPH]": self.stroke_speed("F", "deuce"),
                "Deuce FH In%": self.stroke_in_pct("F", "deuce"),
                "Ad FH Speed [MPH]": self.stroke_speed("F", "ad"),
                "Ad FH In%": self.stroke_in_pct("F", "ad"),
            },
            "Backhand": {
                "BH Speed [MPH]": self.stroke_speed("B"),
                "BH In%": self.stroke_in_pct("B"),
                "Running BH In%": self.bh_in_pct_movement(running=True),
                "Stationary BH In%": self.bh_in_pct_movement(running=False),
            },
            "Net": {
                "Volley Win%": self.volley_win_pct(),
            },
            "Rally": {
                "Rally Shot Width (in meters)": self.rally_width(),
                "Rally Shot Depth (in meters)": self.rally_depth(),
                "Running Rally Shot Width": self.rally_width("running"),
                "Stationary Rally Shot Width": self.rally_width("stationary"),
            },
            "Movement & Footwork": self.movement_block(),
            "Court Position": {
                "Player Distance From Baseline [m]": self.player_distance_from_baseline(),
                "Opponent Distance From Baseline [m]": self.opponent_distance_from_baseline(),
            },
            "Pressure & Big Points": {
                "Break Point Faced Win%": self.break_point_faced(),
                "Break Point Opportunity Win%": self.break_point_opportunity(),
                "Pressure Point Faced Win%": self.pressure_point_faced(),
                "Pressure Point Opportunity Win%": self.pressure_point_opportunity(),
            },
            "Overall Win%": {
                "Overall Serve Win%": self.overall_serve_win(),
                "Overall Return Win%": self.overall_return_win(),
            },
            "Big-Point & +1 Ratios": {
                "Break Point Faced Win% / Overall Serve Win%":
                    ratio_metric(self.break_point_faced(), self.overall_serve_win()),
                "Break Point Opportunity Win% / Overall Return Win%":
                    ratio_metric(self.break_point_opportunity(), self.overall_return_win()),
                "1st Serve Return +1 Win% / 1st Serve Return Win%":
                    ratio_metric(self.return_plus1_win(1), self.return_win(1)),
                "2nd Serve Return +1 Win% / 2nd Serve Return Win%":
                    ratio_metric(self.return_plus1_win(2), self.return_win(2)),
                "Pressure Point Faced Win% / Overall Serve Win%":
                    ratio_metric(self.pressure_point_faced(), self.overall_serve_win()),
                "Pressure Point Opportunity Win% / Overall Return Win%":
                    ratio_metric(self.pressure_point_opportunity(), self.overall_return_win()),
            },
        }


# ============================ ORCHESTRATION ================================= #


def _read_any(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".parquet":
        return pd.read_parquet(path)
    if ext in (".csv", ".tsv"):
        return pd.read_csv(path, sep="\t" if ext == ".tsv" else ",")
    raise ValueError(f"Unsupported data file type: {ext}")


def get_opponent_name(df, player):
    for col in ("server_name", "receiver_name", "PLAYER_HIT"):
        if col in df.columns:
            names = [n for n in df[col].dropna().unique() if n != player]
            if names:
                return names[0]
    return None


def get_surface(df):
    if "surface" in df.columns and len(df):
        vals = df["surface"].dropna().unique()
        if len(vals):
            return str(vals[0])
    return None


def resolve_name(df, name):
    """Match a provided player name to the exact spelling used in the data."""
    candidates = set()
    for col in ("PLAYER_HIT", "server_name", "receiver_name"):
        if col in df.columns:
            candidates.update(str(x) for x in df[col].dropna().unique())
    if name in candidates:
        return name
    low = {c.lower(): c for c in candidates}
    if name.lower() in low:
        return low[name.lower()]
    # last resort: substring match
    for c in candidates:
        if name.lower() in c.lower() or c.lower() in name.lower():
            return c
    return name


def compute_match_metrics(player_name, match_id, serves_df, movement_df=None):
    """Compute metrics for the player and opponent in `match_id`.

    serves_df   : every serve/return event across all points (serve, return,
                  +1 win, pressure, overall-win metrics).
    movement_df : rally shots for points with complete movement tracking
                  (forehand/backhand, net, rally, movement, court position).
                  Defaults to serves_df if not supplied.
    """
    if movement_df is None:
        movement_df = serves_df
    if "match_id" in serves_df.columns:
        serves_df = serves_df[serves_df.match_id == match_id]
    if "match_id" in movement_df.columns:
        movement_df = movement_df[movement_df.match_id == match_id]
    if serves_df.empty:
        raise ValueError(f"No serves_df rows found for match_id={match_id!r}")

    player_name = resolve_name(serves_df, player_name)
    opponent_name = get_opponent_name(serves_df, player_name)
    player_block = MatchMetrics(player_name, serves_df, movement_df).compute()
    opponent_block = (
        MatchMetrics(opponent_name, serves_df, movement_df).compute()
        if opponent_name is not None else None
    )
    return {
        "Match ID": match_id,
        "Player": player_name,
        "Opponent": opponent_name,
        "Surface": get_surface(serves_df),
        player_name: player_block,
        opponent_name: opponent_block,
    }


def main():
    ap = argparse.ArgumentParser(description="Compute UTR feature-list metrics for a player in a match.")
    ap.add_argument("--player-name", required=True)
    ap.add_argument("--match-id", required=True)
    ap.add_argument("--serves-data", default=None, help="serves_df: serve/return events, all points")
    ap.add_argument("--movement-data", default=None, help="movement_df: rally shots, complete-movement points")
    ap.add_argument("--data", default=None, help="single dataframe used for both (fallback)")
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    if not (args.serves_data or args.data):
        ap.error("provide --serves-data (and --movement-data), or --data for both")

    serves_df = _read_any(args.serves_data or args.data)
    movement_df = _read_any(args.movement_data) if args.movement_data else (
        _read_any(args.data) if args.data else serves_df)

    match_id = args.match_id
    if "match_id" in serves_df.columns and pd.api.types.is_integer_dtype(serves_df["match_id"]):
        try:
            match_id = int(match_id)
        except ValueError:
            pass

    result = compute_match_metrics(args.player_name, match_id, serves_df, movement_df)
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"Wrote {args.output}")
    else:
        print(text)


if __name__ == "__main__":
    main()
