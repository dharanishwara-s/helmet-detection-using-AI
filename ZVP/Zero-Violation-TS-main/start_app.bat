@echo off
echo Starting Traffic System...
cd "TRAFFIC SYSTEM"
if %errorlevel% neq 0 (
    echo Error: Could not find 'TRAFFIC SYSTEM' directory.
    pause
    exit /b
)
npm run dev
pause
