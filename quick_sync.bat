@echo off
echo 🚀 Quick Sync to PythonAnywhere via GitHub
echo ==========================================

REM Activate virtual environment
call "%~dp0\.venv\Scripts\activate.bat"

REM Run the GitHub sync script
python "%~dp0\github_sync.py"

echo.
echo 💡 Don't forget to pull changes on PythonAnywhere!
echo    Run this command in PythonAnywhere console:
echo    cd /home/mathserr/mysite && git pull origin main

pause