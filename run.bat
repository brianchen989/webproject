@echo off
cd /d "%~dp0"

IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Running application...
python main.py
pause
