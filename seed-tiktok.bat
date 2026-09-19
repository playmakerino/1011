@echo off
REM Cap nhat danh sach video TikTok (cach browser - cach duy nhat con chay duoc).
REM Chi 1 file nay lo tat ca: copy script, mo TikTok, lay file dump, merge, push.
REM
REM CACH DUNG:
REM   1. Double-click file nay. No tu copy script va mo trang TikTok.
REM   2. Trong Chrome: F12 -> tab Console -> bam vao vung Console -> Ctrl+V -> Enter.
REM      (Lan dau Chrome chan paste: go  allow pasting  roi Enter, xong Ctrl+V lai.)
REM      Cho toi khi Console hien: done - tt_dump.json saved  (vai giay; file nam tren Desktop).
REM      Neu no hien "download failed" thi go dong lenh no in ra, Enter, roi moi sang buoc 3.
REM   3. Quay lai cua so nay, nhan phim bat ky. Xong (no tu merge + push).
setlocal
cd /d "%~dp0"
if not exist scratch md scratch >nul 2>&1

echo === Buoc 1: copy script + mo TikTok ===
type nul > scratch\seed.start
powershell -NoProfile -Command "Get-Content -Raw -Encoding UTF8 'scripts\tiktok-seed.browser.js' | Set-Clipboard"
start "" "https://www.tiktok.com/@teubongday"
echo.
echo   Trong Chrome vua mo:  F12  ->  tab Console  ->  bam vao Console  ->  Ctrl+V  ->  Enter
echo   (lan dau Chrome chan paste: go  allow pasting  roi Enter, xong Ctrl+V lai)
echo   Cho toi khi Console hien:  done - tt_dump.json saved ...
echo   (neu Chrome hoi noi luu file: luu ra Desktop, giu ten tt_dump.json)
echo   (neu hien "download failed": go dong lenh no in ra, Enter, roi moi quay lai day)
echo.
echo Sau khi thay chu "done", quay lai day:
pause

echo.
echo === Buoc 2: lay file dump -> merge -> push ===
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\tiktok-seed-collect.ps1
if errorlevel 1 (
  echo Chay lai, va nho cho Console hien "done" TRUOC khi nhan phim o buoc 1.
  pause
  exit /b 1
)
python scripts\tiktok_seed_merge.py scratch\tt_dump.json tiktok\teubongday.json
if errorlevel 1 (
  echo [LOI] File dump khong phai JSON hop le.
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
