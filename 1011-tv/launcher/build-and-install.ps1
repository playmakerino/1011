# Builds 1011 TV and installs it on the box as the default home screen.
#
# Usage: launcher\build-and-install.ps1 -TvHost 192.168.1.2
#        (or set $env:TV_HOST). JAVA_HOME and the Android SDK default to the portable copies in
#        %USERPROFILE%\.cleanyourtv-build (jdk-17*, sdk), so nothing has to be installed system-wide.
param(
    [string]$TvHost = $env:TV_HOST
)
$ErrorActionPreference = 'Stop'
# Pipe plain UTF-8 to native commands; the default here prepends a BOM that corrupts the first command.
$OutputEncoding = New-Object System.Text.UTF8Encoding $false
if (-not $TvHost) { throw 'pass -TvHost <tv ip> or set $env:TV_HOST' }
$env:TV_HOST = $TvHost
Set-Location $PSScriptRoot
# cmd and python resolve relative paths against the process directory, which Set-Location does not move.
[Environment]::CurrentDirectory = $PSScriptRoot

$tools = Join-Path $env:USERPROFILE '.cleanyourtv-build'
if (-not $env:JAVA_HOME -or -not (Test-Path "$env:JAVA_HOME\bin\java.exe")) {
    $jdk = Get-ChildItem $tools -Directory -Filter 'jdk-17*' -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $jdk) { throw "Set JAVA_HOME to a JDK 17, or unpack one into $tools" }
    $env:JAVA_HOME = $jdk.FullName
}
if (-not (Test-Path local.properties)) {
    $sdk = if ($env:ANDROID_HOME) { $env:ANDROID_HOME } else { Join-Path $tools 'sdk' }
    "sdk.dir=$($sdk -replace '\\', '/')" | Out-File -Encoding ascii local.properties
}

# As a separate process: Windows PowerShell 5.1 turns Gradle's warnings on stderr into errors under Stop.
$gradle = Start-Process -FilePath (Join-Path $PSScriptRoot 'gradlew.bat') -WorkingDirectory $PSScriptRoot `
    -ArgumentList 'assembleRelease', '-q', '--console=plain' -NoNewWindow -Wait -PassThru
if ($gradle.ExitCode -ne 0) { throw 'Gradle build failed' }

$py = '..\tools\venv\Scripts\python.exe'
$apk = 'app\build\outputs\apk\release\app-release.apk'
& $py -I ..\tools\b64push.py $apk /data/local/tmp/tvhome.apk
if ($LASTEXITCODE -ne 0) { throw 'APK upload failed' }
$out = & $py -I ..\tools\tv.py 'pm install -r /data/local/tmp/tvhome.apk; rm -f /data/local/tmp/tvhome.apk'
Write-Host $out
if ("$out" -notmatch 'Success') { throw 'pm install failed' }

@(
    # The gear's network row reads the Wi-Fi name, which needs location since Android 10.
    'pm grant com.gathin.tvhome android.permission.ACCESS_FINE_LOCATION 2>/dev/null; echo location-granted',
    # The grid is sorted by how often each app is opened (LaunchCounts).
    'appops set com.gathin.tvhome GET_USAGE_STATS allow; echo usage-stats-allowed',
    'cmd package compile -m speed -f com.gathin.tvhome',
    'am force-stop com.gathin.tvhome',
    'cmd package set-home-activity --user 0 com.gathin.tvhome/.MainActivity'
) | & $py -I ..\tools\tv.py --batch
$start = (& $py -I ..\tools\tv.py 'am start -W -a android.intent.action.MAIN -c android.intent.category.HOME -n com.gathin.tvhome/.MainActivity') -join "`n"
if ($start -notmatch 'Status: ok') { throw "1011 TV did not start:`n$start" }
$homeNow = (& $py -I ..\tools\tv.py 'cmd package resolve-activity --brief -c android.intent.category.HOME -a android.intent.action.MAIN' | Select-Object -Last 1).Trim()
if ($homeNow -notlike 'com.gathin.tvhome/*') { throw "Home resolves to '$homeNow', not to 1011 TV" }
Write-Host "Installed. Home is $homeNow"
