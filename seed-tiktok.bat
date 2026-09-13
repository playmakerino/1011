@echo off
REM Cap nhat danh sach video TikTok (cach browser - cach duy nhat con chay duoc).
REM Chi 1 file nay lo tat ca: copy script, mo TikTok, doc clipboard, merge, push.
REM
REM CACH DUNG:
REM   1. Double-click file nay. No tu copy script va mo trang TikTok.
REM   2. Trong Chrome: F12 -> tab Console -> bam vao vung Console -> Ctrl+V -> Enter.
REM      Cho toi khi Console hien: done - dump copied to clipboard  (~1 phut).
REM   3. Quay lai cua so nay, nhan phim bat ky. Xong (no tu merge + push).
setlocal
cd /d "%~dp0"
if not exist scratch md scratch >nul 2>&1

echo === Buoc 1: copy script + mo TikTok ===
powershell -NoProfile -Command "Get-Content -Raw 'scripts\tiktok-seed.browser.js' | Set-Clipboard"
start "" "https://www.tiktok.com/@teubongday"
echo.
echo   Trong Chrome vua mo:  F12  ->  tab Console  ->  bam vao Console  ->  Ctrl+V  ->  Enter
echo   Cho toi khi Console hien:  done - dump copied to clipboard
echo.
echo Sau khi thay chu "done", quay lai day:
pause

echo.
echo === Buoc 2: doc clipboard -> merge -> push ===
powershell -NoProfile -Command "$t=Get-Clipboard -Raw; [IO.File]::WriteAllText((Join-Path (Get-Location) 'scratch\tt_dump.json'), $t, (New-Object Text.UTF8Encoding($false)))"
python scripts\tiktok_seed_merge.py scratch\tt_dump.json tiktok\teubongday.json
if errorlevel 1 (
  echo [LOI] Clipboard khong phai dump JSON hop le.
  echo Chay lai, va nho cho Console hien "done" TRUOC khi nhan phim o buoc 1.
  pause
  exit /b 1
)

git add tiktok\teubongday.json
git diff --cached --quiet && (echo Khong co video moi. & pause & exit /b 0)
git commit -m "tiktok: refresh teubongday list (browser seed)"
git push
if errorlevel 1 (
  echo [LOI PUSH] Merge OK nhung push that bai - kiem tra mang/git.
  pause
  exit /b 1
)

echo.
echo [XONG] Da cap nhat va push. App co ban moi sau ~1 phut.
pause
