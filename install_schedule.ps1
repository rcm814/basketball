$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
Set-Location $root
py -m venv .venv
if ($LASTEXITCODE -ne 0) { throw 'Python setup failed' }
$python = Join-Path $root '.venv\Scripts\python.exe'
& $python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
& $python -m playwright install chromium
if ($LASTEXITCODE -ne 0) { throw 'Browser installation failed' }
# First scrape must succeed before enabling the recurring task.
& $python scraper.py
if ($LASTEXITCODE -ne 0) { throw 'First scrape failed; schedule has not been installed' }
$action = New-ScheduledTaskAction -Execute $python -Argument ('"' + (Join-Path $root 'scraper.py') + '"') -WorkingDirectory $root
$trigger = New-ScheduledTaskTrigger -Daily -DaysInterval 3 -At '09:00'
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 1)
Register-ScheduledTask -TaskName 'Basketball Flashscore CSV' -Action $action -Trigger $trigger -Settings $settings -Description 'Collect previous 3 completed days into local basketball CSV files' -Force
Write-Host 'Installed: Basketball Flashscore CSV. Runs every 3 days at 09:00 local time when your user session is available.'
