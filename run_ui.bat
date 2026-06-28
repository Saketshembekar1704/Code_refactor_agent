@echo off
cd /d "%~dp0"
set "VENV_STREAMLIT=venv\Scripts\streamlit.exe"

echo 🚀 Launching Code Refactor Agent UI...
if not exist "%VENV_STREAMLIT%" (
    echo ❌ Streamlit not found. Please ensure the virtual environment is set up.
    pause
    exit /b 1
)

"%VENV_STREAMLIT%" run ui\streamlit_ui.py
pause
