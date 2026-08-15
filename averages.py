"""Reference averages for the post-match report.

Two averages per player and stat:
- year: the player's weighted average on the match's surface in the match's
  year (falls back to their most recent year with matches on that surface)
- top10: weighted average of the tour's top-10 players on that surface

Values are weighted by each stat's shot/rally count (the *_total columns), the
same weighting the shot evolution reports use.
"""
import json
import re
from pathlib import Path

from report_util_new import leaderboard3

APP_DIR = Path(__file__).parent

with open(APP_DIR / 'wta_players.json') as f:
    WTA_PLAYERS = set(json.load(f))

# EDIT HERE to keep the reference groups current.
TOP_10 = {
    'ATP': ['SINNER', 'ALCARAZ', 'ZVEREV', 'DJOKOVIC', 'FRITZ',
            'SHELTON', 'RUUD', 'MEDVEDEV', 'DE MINAUR', 'RUNE'],
    'WTA': ['SABALENKA', 'SWIATEK', 'GAUFF', 'PEGULA', 'ZHENG',
            'KEYS', 'RYBAKINA', 'NAVARRO', 'PAOLINI', 'ANDREEVA'],
}

_YEAR_RE = re.compile(r'(20\d{2})')

def _match_year(match_id):
    m = _YEAR_RE.search(match_id)
    return m.group(1) if m else None


_REAL_SURFACES = {'hard', 'clay', 'grass'}

_all_rows = leaderboard3[leaderboard3.sets == 'ALL'].copy()
_all_rows['year'] = _all_rows.match_id.map(_match_year)
# surface values are mixed-case and include 'ALL' pseudo-rows for combined reports
_all_rows['surface_norm'] = _all_rows.surface.astype(str).str.lower()


def _weighted(rows, keys):
    out = {}
    for k in keys:
        if k in rows.columns and f'{k}_total' in rows.columns:
            totals = rows[f'{k}_total'].astype(float)
            values = rows[k].astype(float)
            weight = totals.sum()
            out[k] = float((values * totals).sum() / weight) if weight > 0 else float('nan')
        else:
            out[k] = float('nan')
    return out


def compute_averages(player, match_id, keys):
    """Return {'year': {...}, 'year_label': str, 'top10': {...}, 'top10_label': str}."""
    match_rows = _all_rows[_all_rows.match_id == match_id]
    if not len(match_rows):
        return None
    surface = str(match_rows.surface_norm.iloc[0])
    if surface not in _REAL_SURFACES:
        return None  # combined/pseudo reports have no meaningful surface reference
    match_year = _match_year(match_id)

    on_surface = _all_rows[(_all_rows.player_name == player) & (_all_rows.surface_norm == surface)]
    years = sorted(y for y in on_surface.year.dropna().unique())
    use_year = match_year if match_year in years else (years[-1] if years else None)
    year_rows = on_surface[on_surface.year == use_year]

    tour = 'WTA' if player in WTA_PLAYERS else 'ATP'
    top_rows = _all_rows[(_all_rows.player_name.isin(TOP_10[tour])) & (_all_rows.surface_norm == surface)]

    surface_label = str(surface).upper()
    return {
        'year': _weighted(year_rows, keys),
        'year_label': f'{use_year} {surface_label} AVG' if use_year else 'YEAR AVG',
        'top10': _weighted(top_rows, keys),
        'top10_label': f'{tour} TOP 10 {surface_label} AVG',
    }
