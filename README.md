# Basketball Flashscore scraper

Imports the configured league Results history from oldest to newest. Expands Show more matches until exhausted, with a configurable safety limit. Existing CSV match IDs are skipped and existing rows, scores, notes and tags remain untouched. Only unseen IDs are added. There is no date lookback filter; missed runs catch up from available history. Today’s completed results can also be imported.

## Windows setup

Install Python 3.11+, download this repository, and open PowerShell in its permanent folder:

```powershell
powershell -ExecutionPolicy Bypass -File .\install_schedule.ps1
```

Installs dependencies, attempts a first scrape, then schedules runs every 3 days at 09:00 PC local time. PC must be on with your user session available. The schedule starts missed tasks when available.

## Run

```powershell
.\.venv\Scripts\python.exe .\scraper.py
```

Output: data/games.csv, data/team_stats.csv, data/league_stats.csv and data/basketball_data.xlsx. Close Excel before running. Keep data/games.csv to preserve history. To rebuild statistics after edits, run with --rebuild-only.

Configure league_urls and max_show_more_clicks in config.json. If the loading limit is reached, the run fails without modifying the CSV; increase the limit to fetch more history. Only the currently configured Results pages are imported; archived seasons require their own URLs. Scraper failures on missing teams/dates/quarters leave the CSV unchanged. Today’s incomplete games can trigger a missing-quarter error if present on Results pages.

Existing IDs are not refreshed, so score corrections on Flashscore must be edited manually in your CSV. Date rollover and duplicate/edit preservation are tested; current team/date selectors have been checked against live page markup, but the full new pagination run has not been tested end to end.
