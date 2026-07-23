# GSA Shot Evolution Interface

Standalone NiceGUI app for building Shot Quality Evolution reports. Works entirely
from local files — no database or Azure storage.

## What's in here

| File | Purpose |
|---|---|
| `main.py` | The web interface (column builder + report creation) |
| `report_core.py` | Loads the leaderboard parquet and computes each column's stats |
| `card.py` | Stat definitions and the weighted-average calculator |
| `report_render.py` | Jinja2 rendering of the report (stat order + pretty names) |
| `convert_gsa_report.py` | Post-processes the rendered HTML into the final styled report |
| `reportnew.html` | Report template |
| `all_data2.json` | Match metadata used for filtering (player, opponent, year, tournament, surface) |
| `leaderboard_haddad_new.parquet` | Per-match stats leaderboard |
| `lefties.json` | Left-handed players (for the opponent-handedness filter) |
| `reports/` | Generated reports are written here and served at `/reports/...` |

## Multi-player columns

Each column's player select accepts **multiple players**. When more than one is
selected, their matches are pooled and every stat is a weighted average over the
pooled shots/rallies — the players are treated as if they were a single player.

## Run locally

```bash
pip install -r requirements.txt
python main.py            # http://localhost:8080
```

## Deploy to Render

1. Put this folder in its own git repo and push it to GitHub:
   ```bash
   cd shot_evolution_app
   git init && git add . && git commit -m "Shot evolution interface"
   gh repo create gsa-shot-evolution --private --source=. --push
   ```
2. In the Render dashboard: **New → Web Service**, connect the repo
   (or click **New → Blueprint** and Render will pick up `render.yaml` automatically).
3. If configuring manually, use:
   - Runtime: **Python 3**
   - Build command: `pip install -r requirements.txt`
   - Start command: `python main.py`
   - Instance type: **Starter** (512 MB). The free tier can work but is tight —
     the parquet + pandas need a few hundred MB, and free instances spin down
     after 15 min of inactivity.
4. Deploy. The app reads the `PORT` env var Render sets automatically.

Notes:
- Render's disk is **ephemeral**: generated reports in `reports/` disappear on
  each deploy/restart. Fine for now since reports are regenerated on demand;
  add a Render Disk or object storage later if permanent links are needed.
- To update data, replace `all_data2.json` / `leaderboard_haddad_new.parquet`
  and push — Render redeploys on every push.
