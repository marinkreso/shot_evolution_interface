"""
cv_adapter.py
=============

Turn a raw CV (computer-vision / manual-charting) shot dataframe into the
Hawk-Eye-shaped dataframe that utr_match_metrics5.py consumes.

Usage
-----
    import pandas as pd
    from cv_adapter import add_he_features
    from utr_match_metrics5 import compute_match_metrics

    cvdf = pd.read_parquet("match.parquet")
    df = add_he_features(cvdf)
    result = compute_match_metrics("rybakina", df["match_id"].iloc[0], df)

Maps (CV -> Hawk-Eye)
---------------------
  impact_player -> PLAYER_HIT        point_winner -> PLAYER_WIN_NAME
  server        -> server_name       returner     -> receiver_name
  serve         -> serve_number      (see serve-number note below)
  shot          -> shot_no           set/game/point -> set_no/game_no/point_no
  hit_x/_y      -> CONTACT_X_abs / CONTACT_Y_mirrored
  bounce_x/_y   -> REBOUND_X_abs / REBOUND_Y_mirrored
  deuce_or_ad   -> serve_deuce_or_ad
  stroke        -> shot_type (F/B)   placement_gsa -> is_shot_in, serve_direction

Serve number (heuristic — CV counts let/replay serves)
------------------------------------------------------
  serve == 1 -> 1st serve; serve in {2,3,...,0} -> 2nd serve. A "2nd serve" hit
  faster than SERVE_1ST_SPEED_KMH is treated as a re-taken 1st serve (a let).
  This is rough; refine later with serve_type / timing if needed.

Pressure (derived from the score, mirrors the charting pipeline)
----------------------------------------------------------------
  Per match we first learn which player is on the LEFT of the `gamescore` string
  (from the first decisive point: the winner is the side that pulled ahead). A
  point is a break point when the game-point side of the gamescore is the
  RECEIVER; a pressure point adds 30-30/40-40/deuce-type scores and ALL tiebreak
  points (detected via games 6-6). Break points are always pressure points too.

NOT available from CV (utr_match_metrics5 reports these as NA)
-------------------------------------------------------------
  Per-frame tracking. CV has ONE location per shot (player_location_*,
  receiver_location_*) + time_passed, so movement is per-shot: Start-End
  speed/accel compute, but foot-speed Max / per-sample Average and the whole
  Reaction-Time block (time to move 0.5/1 m, time to peak velocity) cannot.
  spinRPM is absent; utr_match_metrics5 detects dropshot runs from events.shot.
"""

import warnings
from collections import Counter

import numpy as np
import pandas as pd

SERVE_1ST_SPEED_KMH = 190.0          # a "2nd serve" faster than this is a re-taken 1st serve
PLAYER_LEFT_MIN_AGREEMENT = 0.8      # warn if < this share of tied-point votes agree on the side

# CV serve placement -> Hawk-Eye serve_direction letter
_SERVE_DIR = {"WIDE": "W", "BODY": "B", "T": "T"}

_RALLY_KEYS = ["match_id", "set", "game", "point", "serve"]
_POINT_KEYS = ["match_id", "set", "game", "point", "serve"]
_ORDER_KEYS = ["match_id", "set", "game", "point", "serve", "shot"]

# --- gamescore sets (left-oriented and its mirror), from the charting pipeline - #
_BREAK_LEFT = {"4015", "4000", "4030", "A40", "Ad40", "AD40"}
_BREAK_RIGHT = {"1540", "0040", "3040", "40A", "40Ad", "40AD"}
_PRESS_LEFT = {"3030", "4040", "4015", "4000", "4030", "Ad40", "40A", "AD40", "3015"}
_PRESS_RIGHT = {"0040", "3040", "40Ad", "1530", "3030", "4040", "1540"}


def _int_safe(x):
    """Score token -> comparable number ('Ad' -> 45)."""
    s = str(x).strip().lower()
    if s in ("ad", "a", "adv"):
        return 45
    try:
        return int(s)
    except ValueError:
        return None


def _parse_gs(score_str):
    """Split a gamescore like '3015' into (30, 15). Two-char tokens; 'Ad' = 45."""
    if not isinstance(score_str, str) or len(score_str) < 3:
        return None, None
    return _int_safe(score_str[:2]), _int_safe(score_str[2:])


def _tied(score_str):
    """True if a gamescore parses to equal left/right (0-0, 15-15, 30-30, 40-40)."""
    l, r = _parse_gs(score_str)
    return l is not None and r is not None and l == r


def _left_player_per_match(df):
    """Learn which player is on the LEFT of `gamescore`, per match, by MAJORITY
    VOTE over every point that starts from a TIED score (0-0, 15-15, 30-30, deuce).
    After a tied point the winner is unambiguously the side that pulled ahead, so
    gamescore_next reveals which side (left/right) the winner is on. Voting over
    all such points (instead of trusting the first) is the consistency check; a
    warning fires if the votes for a match disagree beyond PLAYER_LEFT_MIN_AGREEMENT.
    """
    order = [c for c in _ORDER_KEYS if c in df.columns]
    pts = (df.sort_values(order)
             .drop_duplicates([c for c in _POINT_KEYS if c in df.columns])
             .copy())
    pts["_gsn"] = pts.groupby("match_id")["gamescore"].shift(-1)
    left = {}
    for m, grp in pts.groupby("match_id"):
        names = [str(n).lower() for n in pd.unique(grp["server"].dropna())]
        votes = Counter()
        for _, r in grp.iterrows():
            if not _tied(r.get("gamescore")):        # only vote from tied -> untied
                continue
            l, rr = _parse_gs(r.get("_gsn"))
            if l is None or rr is None or l == rr:
                continue
            winner = str(r["point_winner"]).lower()
            if l > rr:                               # winner pulled ahead on the left
                votes[winner] += 1
            else:                                    # winner pulled ahead on the right
                others = [n for n in names if n != winner]
                if others:
                    votes[others[0]] += 1
        if not votes:
            left[m] = None
            continue
        best, top = votes.most_common(1)[0]
        total = sum(votes.values())
        left[m] = best
        if total and top / total < PLAYER_LEFT_MIN_AGREEMENT:
            warnings.warn(
                f"[cv_adapter] gamescore left/right side for match {m} is ambiguous: "
                f"votes={dict(votes)} -> using '{best}' ({top}/{total} agree). "
                f"Break/pressure flags for this match may be unreliable.",
                stacklevel=2)
    return left


def _derive_pressure(df):
    """(is_break_point, is_pressure_point) int Series from the score."""
    if "gamescore" not in df.columns or "server" not in df.columns:
        z = pd.Series(0, index=df.index)
        return z, z

    left_player = df["match_id"].map(_left_player_per_match(df))
    server_left = df["server"].astype(str).str.lower() == left_player
    gs = df["gamescore"].astype(str)

    is_break = (gs.isin(_BREAK_LEFT) & ~server_left) | (gs.isin(_BREAK_RIGHT) & server_left)
    press = (gs.isin(_PRESS_LEFT) & ~server_left) | (gs.isin(_PRESS_RIGHT) & server_left)

    tiebreak = pd.Series(False, index=df.index)
    if "Player1_score_game" in df.columns and "Player2_score_game" in df.columns:
        g1 = pd.to_numeric(df["Player1_score_game"], errors="coerce")
        g2 = pd.to_numeric(df["Player2_score_game"], errors="coerce")
        tiebreak = (g1 == 6) & (g2 == 6)

    is_pressure = press | is_break | tiebreak
    return is_break.astype(int), is_pressure.astype(int)


def _serve_number(df):
    """1st/2nd serve flag. serve==1 -> 1; else -> 2; a '2nd serve' faster than
    SERVE_1ST_SPEED_KMH (on the serve row) is promoted to 1 (re-taken 1st)."""
    serve = pd.to_numeric(df["serve"], errors="coerce")
    sn = np.where(serve == 1, 1, 2)
    sn = pd.Series(sn, index=df.index)
    if "SPEED" in df.columns and "shot" in df.columns and "rally_id" in df.columns:
        srv = df[df["shot"] == 1]
        srv_speed = srv.groupby("rally_id")["SPEED"].first()
        rally_srv_speed = df["rally_id"].map(srv_speed)
        promote = (sn == 2) & (rally_srv_speed > SERVE_1ST_SPEED_KMH)
        sn = sn.mask(promote, 1)
    return sn.astype(int)


def _drop_noise(df):
    """Drop dead-ball 'Extra' shots, and drop the serve that PRECEDES a >190 km/h
    'second serve' (that fast 2nd serve is a re-taken 1st serve, so the serve
    before it was a let, not a real fault). Needs point_id / rally_id built."""
    if "outcome" in df.columns:
        df = df[df["outcome"].astype(str) != "Extra"].copy()
    need = ("rally_id", "point_id", "serve", "shot", "SPEED")
    if all(c in df.columns for c in need):
        serve_num = pd.to_numeric(df["serve"], errors="coerce")
        srv_speed = df[df["shot"] == 1].groupby("rally_id")["SPEED"].first()
        rally_srv_speed = df["rally_id"].map(srv_speed)
        promoted = (serve_num >= 2) & (rally_srv_speed > SERVE_1ST_SPEED_KMH)
        prom_serves = pd.to_numeric(df.loc[promoted, "serve"], errors="coerce")
        discard = {(p, int(s) - 1) for p, s in zip(df.loc[promoted, "point_id"], prom_serves)
                   if s == s}
        if discard:
            keep = [((p, int(s)) not in discard) if s == s else True
                    for p, s in zip(df["point_id"], serve_num)]
            df = df[pd.Series(keep, index=df.index)].copy()
    return df


def add_he_features(cvdf):
    """Return a copy of `cvdf` with Hawk-Eye-equivalent columns added."""
    df = cvdf.copy()

    # --- identity / key columns (built first; used to drop let/Extra noise) ----
    mid = df["match_id"].astype(str)
    sset, game, point = df["set"].astype(str), df["game"].astype(str), df["point"].astype(str)
    df["point_id"] = mid + "_" + sset + "_" + game + "_" + point
    df["rally_id"] = df["point_id"] + "_" + df["serve"].astype(str)
    df["game_id"] = mid + "_" + sset + "_" + game
    df["set_id"] = mid + "_" + sset

    # drop dead-ball 'Extra' shots and let-serves preceding a fast 2nd serve
    df = _drop_noise(df)

    # --- mirrored coordinates (flip Y when contacted/bounced from the +X half) --
    df["hit_y_mirrored"] = np.where(df["hit_x"] > 0, -df["hit_y"], df["hit_y"])
    df["bounce_y_mirrored"] = np.where(df["bounce_x"] > 0, -df["bounce_y"], df["bounce_y"])
    if "ON_NET_Y" in df.columns:
        df["ON_NET_Y_mirrored"] = np.where(df["bounce_x"] < 0, -df["ON_NET_Y"], df["ON_NET_Y"])

    # --- Hawk-Eye coordinate columns -------------------------------------------
    df["CONTACT_X_abs"] = df["hit_x"].abs()
    df["CONTACT_Y_mirrored"] = df["hit_y_mirrored"]
    df["REBOUND_X_abs"] = df["bounce_x"].abs()
    df["REBOUND_Y_mirrored"] = df["bounce_y_mirrored"]

    # --- key columns (IDs already built above, before _drop_noise) -------------
    df["set_no"] = df["set"]
    df["game_no"] = df["game"]
    df["point_no"] = df["point"]
    df["shot_no"] = df["shot"]
    df["serve_number"] = _serve_number(df)     # 1st/2nd with let handling (see note)

    df["PLAYER_HIT"] = df["impact_player"]
    df["PLAYER_WIN_NAME"] = df["point_winner"]
    df["server_name"] = df["server"]
    if "returner" in df.columns:
        df["receiver_name"] = df["returner"]

    # --- shot descriptors ------------------------------------------------------
    df["is_shot_in"] = (~df["placement_gsa"].str.contains("Out|Net", na=True)).astype(int)
    df["is_shot_serve"] = (df["shot_no"] == 1).astype(int)
    df["shot_type"] = df["stroke"].map(lambda x: x[0].upper() if isinstance(x, str) and x else None)

    # serve_direction (W/B/T) from the serve row's placement, carried on the rally
    serve_place = df.groupby("rally_id")["placement_gsa"].transform("first").astype(str).str.upper()
    df["serve_direction"] = serve_place.map(_SERVE_DIR)

    df["serve_deuce_or_ad"] = df["deuce_or_ad"]

    # --- serve accuracy proxies (matches the manual pipeline) ------------------
    df["distance_from_sideline"] = (8.18 / 2 - df["REBOUND_Y_mirrored"].abs()).abs()
    df["distance_from_side_or_center_line"] = np.minimum(
        df["distance_from_sideline"], df["REBOUND_Y_mirrored"].abs())
    df["INTER_LENGTH"] = 5.47
    df["TOTAL_LENGTH"] = 23.7
    df["distance_from_service_line"] = (df["TOTAL_LENGTH"] / 2
                                        - df["INTER_LENGTH"] - df["REBOUND_X_abs"]).abs()
    df["BASELINE_DISTANCE"] = (11.89 - df["CONTACT_X_abs"]) * -1

    # --- per-shot timing (for movement speed/accel) ----------------------------
    if "Hit_time" in df.columns:
        prev = df.groupby(_RALLY_KEYS)["Hit_time"].shift(1)
        df["time_passed"] = (pd.to_timedelta(df["Hit_time"])
                             - pd.to_timedelta(prev)).dt.total_seconds()

    # --- derived pressure flags ------------------------------------------------
    df["is_break_point"], df["is_pressure_point"] = _derive_pressure(df)

    return df
