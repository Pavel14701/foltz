# Memory commit watcher: logs top-5 commit consumers every 15s.
# Log: mem_watch.log in project root. Start: powershell -File mem_watch.ps1 (hidden)
$log = Join-Path $PSScriptRoot 'mem_watch.log'
while ($true) {
  $os = Get-CimInstance Win32_OperatingSystem
  $used = [math]::Round(($os.TotalVirtualMemorySize - $os.FreeVirtualMemory)/1MB,1)
  $limit = [math]::Round($os.TotalVirtualMemorySize/1MB,1)
  $top = Get-Process | Sort-Object PagedMemorySize64 -Descending | Select-Object -First 5 |
    ForEach-Object { '{0}:{1}MB' -f $_.Name, [math]::Round($_.PagedMemorySize64/1MB) }
  Add-Content -Path $log -Value ("{0} commit {1}/{2} GB | {3}" -f (Get-Date -Format 'HH:mm:ss'), $used, $limit, ($top -join ' '))
  Start-Sleep -Seconds 15
}
