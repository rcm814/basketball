# Basketball Flashscore scraper

Euroleague and Australian NBL are enabled by default. Add more basketball league Results URLs to `league_urls` in config.json. The same games.csv can hold multiple leagues.

Search Flashscore's basketball country directories (search only; choose a result URL explicitly):

```powershell
.\.venv\Scripts\python.exe .\scraper.py --search "NBL" --country australia
.\.venv\Scripts\python.exe .\scraper.py --search "Euroleague"
```

Search without --country scans the country links exposed on Flashscore's basketball directory and can take several minutes. It is not a guarantee of every league or archived season; use a direct Results URL if a league is missing.

Scrape a chosen league into a separate new or existing CSV:

```powershell
.\.venv\Scripts\python.exe .\scraper.py --league-url "https://www.flashscore.com/basketball/australia/nbl/results/" --csv "data/nbl.csv"
```

Repeat --league-url for multiple leagues. These options override configured URLs for that run only. Without options, the existing scheduled command imports all configured leagues into data/games.csv. Statistics and Excel still go to output_directory and reflect the selected CSV.

Existing match IDs and custom CSV columns are preserved. If there are no new IDs, the game CSV is not rewritten. Invalid CSV headers, missing IDs, and duplicate saved IDs fail without replacing the CSV. Only compatible scraper CSVs with match_id are supported.

Validation: offline tests cover URL validation, date parsing, duplicates, existing scores/notes/custom columns, unchanged files on no-op runs, and invalid CSV protection. Live league search and NBL pagination have not been verified in this environment.

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
