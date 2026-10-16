@echo off
cd /d "%~dp0"
if "%~1"=="" (
  echo Hasznalat: run_windows.bat "C:\adatok\csv_light2.zip"
  exit /b 1
)
python src\run_real_validation.py --real-zip "%~1"
pause
