"""CV -> post-match pipeline (phase 1: metric coverage).

Takes a CV match parquet (from fetch_cv_matches.py), adapts it to the
Hawk-Eye shape and runs the leaderboard metric engine (CalculationsFinal5)
fault-tolerantly, reporting which metrics compute and which fail — measured
against the stat keys the post-match page renders (report_util_new data_order).
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# the metric engine was written for pandas 1.x
if not hasattr(pd.DataFrame, 'append'):
    def _df_append(self, other, ignore_index=False):
        other = other if isinstance(other, pd.DataFrame) else pd.DataFrame([other])
        return pd.concat([self, other], ignore_index=ignore_index)
    pd.DataFrame.append = _df_append

HERE = Path(__file__).parent
APP = HERE.parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


calc_mod = _load('calculations_final5', HERE / 'CalculationsFinal5 file.py')
cv_adapter = _load('cv_adapter', HERE / 'cv_adapter (1).py')
joschka = _load('cv_metrics_joschka', HERE / 'cv_metrics_joschka.py')

Calculations = calc_mod.Calculations
FUNCTIONS = calc_mod.functions

_errors = {}
_orig_calculate_all = Calculations.calculate_all


def _tolerant_calculate_all(self, df, df_serve, match_id, sets):
    """calculate_all with a per-metric try/except (CV frames miss HE columns)."""
    new_row = {'player_name': Calculations.PLAYER_NAME,
               'match_id': match_id,
               'opponent_name': self.get_opponent_name(df, match_id),
               'surface': self.get_surface(df, match_id)}
    serve_frame_funcs = calc_mod.Calculations.calculate_all.__doc__  # not used; kept simple below
    for func_name in FUNCTIONS:
        try:
            func = getattr(self, func_name)
            # mirror the original's df/df_serve routing by trying df_serve first
            # for the serve/return in%-style funcs; the original hardcodes the
            # list — we reproduce it via the source list captured at import
            if func_name in _SERVE_FRAME_FUNCS:
                result = func(df_serve)
            else:
                result = func(df)
            if result is not None:
                new_row[func_name] = result[0]
                new_row[f'{func_name}_total'] = result[1]
            else:
                new_row[func_name] = None
                new_row[f'{func_name}_total'] = None
        except Exception as e:
            _errors.setdefault(func_name, str(e)[:120])
            new_row[func_name] = None
            new_row[f'{func_name}_total'] = None
    new_dataset = pd.DataFrame(new_row, index=[0])
    new_dataset['sets'] = sets
    Calculations.results_df = pd.concat([Calculations.results_df, new_dataset], ignore_index=True)


# extract the df_serve-routed function list from the original source
import inspect
import re as _re
_src = inspect.getsource(_orig_calculate_all)
_m = _re.search(r'if func_name in \[(.*?)\]:', _src, _re.S)
_SERVE_FRAME_FUNCS = set(_re.findall(r"'([^']+)'", _m.group(1))) if _m else set()

Calculations.calculate_all = _tolerant_calculate_all


def load_cv_match(parquet_path):
    cvdf = pd.read_parquet(parquet_path)
    df = cv_adapter.add_he_features(cvdf)
    df = joschka.resolve_serve_attempts(df)
    # rally_length and surface expectations of the engine
    if 'surface' not in df.columns:
        df['surface'] = 'hard'
    return df


features = _load('cv_leaderboard_features', HERE / 'cv_leaderboard_features.py')


def resolve_player(df, requested):
    """Map a display name like 'Julieta Pareja' to the frame's name form."""
    req = requested.lower()
    for name in df.PLAYER_HIT.dropna().unique():
        if str(name).lower() in req or req in str(name).lower():
            return name
    raise ValueError(f'{requested} not in frame players {df.PLAYER_HIT.unique()}')


# spin metrics have no CV source (spinRPM is only a gate placeholder): never report them
SPIN_METRICS = [f for f in FUNCTIONS if 'spin' in f or f == 'topspin_slice']


def run_metrics(df, player_name, sets_list=('ALL', 1, 2, 3)):
    """player_name must be the frame's own form (see resolve_player)."""
    frame = features.build_leaderboard_frame(df, player_name)
    Calculations.results_df = pd.DataFrame(columns=Calculations.results_df.columns)
    _errors.clear()
    for sets in sets_list:
        Calculations(player_name, frame, frame, False, sets=sets)
    rows = Calculations.results_df.drop_duplicates(subset=['match_id', 'sets'], keep='first').copy()
    for m in SPIN_METRICS:
        if m in rows.columns:
            rows[m] = None
            rows[f'{m}_total'] = 0
    return rows, dict(_errors)


def page_stat_keys():
    """Stat keys the post-match page renders (from the app's report_util_new)."""
    sys.path.insert(0, str(APP))
    import re
    src = (APP / 'report_util_new.py').read_text()
    m = re.search(r'data_order = \{(.*?)\n    \}', src, re.S)
    return sorted(set(re.findall(r"'([a-z0-9_]+)'", m.group(1)))) if m else []


if __name__ == '__main__':
    parquet = sys.argv[1]
    player = sys.argv[2]
    df = load_cv_match(parquet)
    print('players in frame:', df.PLAYER_HIT.unique())
    player = resolve_player(df, player)
    print('resolved player:', player)
    rows, errors = run_metrics(df, player)
    all_row = rows[rows.sets == 'ALL'].iloc[0]
    computed = [f for f in FUNCTIONS if pd.notna(all_row.get(f))]
    empty = [f for f in FUNCTIONS if f not in computed and f not in errors]
    print(f'\nmetrics: {len(FUNCTIONS)} total | computed: {len(computed)} | empty/None: {len(empty)} | raised: {len(errors)}')
    page_keys = page_stat_keys()
    pk_computed = [k for k in page_keys if k in computed]
    print(f'page stats: {len(page_keys)} needed | computable from CV: {len(pk_computed)}')
    print('\npage stats MISSING from CV:')
    for k in page_keys:
        if k not in pk_computed:
            print('  ', k, '->', errors.get(k, 'None/empty'))
    print('\nsample computed values:')
    for k in pk_computed[:15]:
        print(f'  {k}: {all_row[k]} (n={all_row.get(k + "_total")})')
