# Called by seed-tiktok.bat after the browser script printed "done".
# Picks up the dump the browser script downloaded (tt_dump*.json in Downloads, newer than the marker
# file the .bat wrote at start) and puts it at scratch\tt_dump.json. Falls back to the clipboard for
# the manual copy(...) one-liner. Exit 1 when neither holds a dump.
$ErrorActionPreference = 'Stop'
$marker = 'scratch\seed.start'
$since = if (Test-Path $marker) { (Get-Item $marker).LastWriteTime } else { (Get-Date).AddHours(-1) }
$dl = (New-Object -ComObject Shell.Application).NameSpace('shell:Downloads').Self.Path
$here = (Get-Location).Path
$f = @($here, $dl) | ForEach-Object { Get-ChildItem (Join-Path $_ 'tt_dump*.json') -ErrorAction SilentlyContinue } |
     Where-Object { $_.LastWriteTime -ge $since } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($f) {
  Copy-Item $f.FullName 'scratch\tt_dump.json' -Force
  Remove-Item $f.FullName
  Write-Host ('  lay ' + $f.FullName)
  exit 0
}
$t = Get-Clipboard -Raw
if ($t -and $t.TrimStart().StartsWith('{')) {
  [IO.File]::WriteAllText((Join-Path (Get-Location) 'scratch\tt_dump.json'), $t, (New-Object Text.UTF8Encoding($false)))
  Write-Host '  lay dump tu clipboard'
  exit 0
}
Write-Host ('  [LOI] Khong thay tt_dump*.json moi trong ' + $here + ' hay ' + $dl + ', va clipboard cung khong phai JSON.')
exit 1
