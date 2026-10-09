# Basketball Flashscore scraper

Collect the previous three completed calendar days for the leagues in `config.json` and update a local CSV. Dates use Europe/Budapest. On October 9 this includes October 6, 7 and 8.

## Install and schedule on Windows

Install Python 3.11+ first. Download this repository (Code > Download ZIP), extract it to a permanent folder, open PowerShell in that folder, then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\install_schedule.ps1
```

The installer creates a virtual environment, installs Chromium, performs the first scrape, and only then registers **Basketball Flashscore CSV** in Windows Task Scheduler. It runs every three days at 09:00 PC local time. Keep the folder in place. This task uses your Windows user session: the PC must be on and you must be signed in. A missed trigger runs when available, but its collection window still covers only the previous three days. Longer outages require increasing `lookback_days` temporarily and running manually.

## Local output

- `data/games.csv`: cumulative historical games, updated by match ID without duplicates.
- `data/team_stats.csv`: team quarter average/min/max and final score/allowed statistics.
- `data/league_stats.csv`: combined quarter and game average/min/max.
- `data/basketball_data.xlsx`: Excel view of the same data.

Edit notes and tags in `games.csv`; those are preserved. Scraped score fields are updated when that match is scraped again. Close the files in Excel before a run. Data files stay local and are excluded from Git.

## Manual run / rebuild

```powershell
.\.venv\Scripts\python.exe scraper.py
.\.venv\Scripts\python.exe scraper.py --rebuild-only
```

## Configure

The default league is EuroLeague. Add other league Results URLs in `config.json`. `lookback_days` defaults to 3. `max_show_more_clicks` controls the bounded amount of results history loaded; increase it for very busy leagues or longer backfills.

## Validation and limitations

Date rollover and CSV duplicate/edit preservation have automated tests. The current Flashscore browser extraction has not been validated against a live page in this environment. Site markup may change; missing dates or quarter scores cause the run to fail rather than add unreliable records. Missing result rows also fail without changing the CSV. A league with no games in the collection window adds nothing. Statistics include every stored record; games with missing quarters do not contribute to those quarter statistics. Overtime is the difference between final score and four regulation quarters.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -p "test_*.py"
```

To disable the schedule:

```powershell
Unregister-ScheduledTask -TaskName "Basketball Flashscore CSV" -Confirm:$false
```
