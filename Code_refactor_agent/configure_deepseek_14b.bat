@echo off
REM DeepSeek 14B Configuration Script
REM Save this as: configure_deepseek_14b.bat

echo ============================================================
echo  Configuring for DeepSeek Coder 14B Model
echo ============================================================
echo.

echo 🔍 Checking Ollama status...
tasklist | findstr "ollama" >nul 2>&1
if errorlevel 1 (
    echo ❌ Ollama service is not running
    echo 🚀 Starting Ollama service...
    start /min "Ollama Service" ollama serve
    echo ⏳ Waiting 10 seconds for Ollama to start...
    timeout /t 10 /nobreak >nul
) else (
    echo ✅ Ollama service is running
)

echo.
echo 🔍 Checking available models...
ollama list

echo.
echo 🔍 Looking for DeepSeek 14B model...
ollama list | findstr "14b" >nul 2>&1
if errorlevel 1 (
    echo ❌ DeepSeek 14B model not found in the list above
    echo.
    echo Please check the exact model name from the list above.
    echo Common DeepSeek 14B model names:
    echo - deepseek-coder:14b
    echo - deepseek-coder:14b-instruct  
    echo - deepseek-coder:14b-base
    echo.
    set /p model_name="Enter the exact model name: "
) else (
    echo ✅ DeepSeek 14B model found
    REM Extract the exact model name
    for /f "tokens=1" %%i in ('ollama list ^| findstr "14b"') do set model_name=%%i
)

if "%model_name%"=="" (
    echo ❌ No model name specified
    pause
    exit /b 1
)

echo.
echo 🔧 Configuring for model: %model_name%
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Create updated .env file with DeepSeek 14B settings
echo 📝 Creating configuration file for DeepSeek 14B...
(
echo # Ollama Configuration for DeepSeek Coder 14B
echo OPENAI_API_KEY=ollama
echo OPENAI_API_BASE=http://localhost:11434/v1
echo OPENAI_MODEL_NAME=%model_name%
echo.
echo # CrewAI Settings  
echo CREWAI_TELEMETRY_OPT_OUT=true
echo.
echo # Application Settings
echo OLLAMA_URL=http://localhost:11434/v1
echo OLLAMA_MODEL=%model_name%
echo BACKUP_ENABLED=true
echo MAX_COMPLEXITY_THRESHOLD=10
echo DEFAULT_MODE=analysis
echo.
echo # Performance Settings for 14B Model
echo OLLAMA_NUM_PARALLEL=1
echo OLLAMA_MAX_LOADED_MODELS=1
echo OLLAMA_FLASH_ATTENTION=1
) > .env

echo ✅ Configuration file updated

echo.
echo 🧪 Testing DeepSeek 14B model...
echo print("# Test code analysis") | ollama run %model_name% 2>nul
if errorlevel 1 (
    echo ❌ Model test failed
    echo Please ensure the model is properly installed:
    echo ollama run %model_name%
) else (
    echo ✅ Model is responding correctly
)

echo.
echo 🔍 Testing API connection with Python...
python -c "
import os
os.environ['OPENAI_API_KEY'] = 'ollama'
os.environ['OPENAI_API_BASE'] = 'http://localhost:11434/v1'
os.environ['OPENAI_MODEL_NAME'] = '%model_name%'

try:
    import requests
    response = requests.get('http://localhost:11434/api/tags', timeout=10)
    if response.status_code == 200:
        print('✅ Python-Ollama connection successful')
        models = response.json().get('models', [])
        deepseek_models = [m for m in models if '14b' in m.get('name', '').lower()]
        if deepseek_models:
            print(f'✅ Found DeepSeek 14B models: {[m[\"name\"] for m in deepseek_models]}')
        else:
            print('⚠️  No 14B models found in API response')
    else:
        print(f'❌ API returned status: {response.status_code}')
except Exception as e:
    print(f'❌ Connection test failed: {e}')
"

echo.
echo 🚀 Testing the refactoring system...
python -c "
import sys
import os
sys.path.append('.')

# Set environment variables
os.environ['OPENAI_API_KEY'] = 'ollama'
os.environ['OPENAI_API_BASE'] = 'http://localhost:11434/v1' 
os.environ['OPENAI_MODEL_NAME'] = '%model_name%'

try:
    from crew.refactor_crew import RefactorCrew
    print('✅ RefactorCrew import successful')
    print('✅ System is ready to use with DeepSeek 14B')
except Exception as e:
    print(f'❌ System test failed: {e}')
"

echo.
echo ============================================================
echo  🎉 DeepSeek 14B Configuration Complete!
echo ============================================================
echo.
echo 📊 Model Configuration:
echo   Model Name: %model_name%
echo   API Endpoint: http://localhost:11434/v1
echo   Performance: Optimized for 14B model
echo.
echo 🚀 Ready to use! Try:
echo   python main.py --target-dir .\test_project --mode analysis
echo.
echo 💡 Note: The 14B model is more powerful but may be slower than 6.7B
echo    Ensure you have adequate RAM (16GB+ recommended)
echo.
pause