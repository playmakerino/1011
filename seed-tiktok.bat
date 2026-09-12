@echo off
REM Cap nhat danh sach video TikTok bang cach seed tu trinh duyet (cach duy nhat con chay duoc).
REM yt-dlp da bi TikTok chan (tra body rong o moi IP) nen khong con Action tu dong nua.
REM
REM CACH DUNG (3 buoc):
REM   1. Mo https://www.tiktok.com/@teubongday trong Chrome -> F12 -> tab Console.
REM      Mo file scripts\tiktok-seed.browser.js, copy TOAN BO, dan vao Console, Enter.
REM      Cho toi khi hien "done - dump copied to clipboard" (~1 phut, no tu scroll).
REM   2. Mo Notepad, dan (Ctrl+V), luu thanh:  scratch\tt_dump.json  (trong thu muc nay).
REM   3. Chay file .bat nay (double-click). No merge + commit + push.
setlocal
cd /d "%~dp0"

if not exist "scratch\tt_dump.json" (
  echo [THIEU FILE] Chua thay scratch\tt_dump.json
  echo Lam buoc 1-2 o tren truoc: chay script trong Console roi luu clipboard thanh scratch\tt_dump.json
  pause
  exit /b 1
)

echo === Merge dump vao tiktok\teubongday.json ===
python scripts\tiktok_seed_merge.py scratch\tt_dump.json tiktok\teubongday.json
if errorlevel 1 (
  echo [LOI] Merge that bai - kiem tra file scratch\tt_dump.json co dung JSON khong.
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
echo [XONG] Da cap nhat va push. GitHub Pages co ban moi sau ~1 phut.
pause
