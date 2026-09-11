@echo off
REM Bam de cap nhat danh sach video TikTok roi push len GitHub (GitHub Pages tu serve lai).
REM Chay tu chinh IP nha (residential) nen ti le lot cao hon GitHub Actions.
setlocal
cd /d "%~dp0"

echo === Cap nhat yt-dlp (de theo kip thay doi cua TikTok) ===
python -m pip install -q -U yt-dlp

echo.
echo === Scrape @teubongday ===
REM 50 video moi nhat, gop vao danh sach san co (bat khong chay hang ngay nhu Action, nen lay rong hon)
python scripts\tiktok.py "tiktokuser:MS4wLjABAAAAuBR1Xj56P4gfYMCiv4Bf-PzCBOtKgPBhmBlGoRDnKFftCaINmyjKruz891I41gsu" tiktok\teubongday.json --limit 50
if errorlevel 1 (
  echo.
  echo [THAT BAI] TikTok chan/throttle - file cu giu nguyen, chua push. Thu lai sau vai phut.
  pause
  exit /b 1
)

git add tiktok\teubongday.json
git diff --cached --quiet && (echo Khong co video moi. & pause & exit /b 0)
git commit -m "tiktok: refresh teubongday list (manual)"
git push
if errorlevel 1 (
  echo.
  echo [LOI PUSH] Scrape OK nhung push that bai - kiem tra mang/git.
  pause
  exit /b 1
)

echo.
echo [XONG] Da cap nhat va push. GitHub Pages se co ban moi sau ~1 phut.
pause
