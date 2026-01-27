@echo off
REM Ollama Service Manager for Windows
REM Save this as: manage_ollama.bat

echo ============================================================
echo  Ollama Service Manager - Windows
echo ============================================================
echo.

:MENU
echo Choose an option:
echo 1. Check Ollama Status
echo 2. Start Ollama Service  
echo 3. Stop Ollama Service
echo 4. Restart Ollama Service
echo 5. Test API Connection
echo 6. Show Available Models
echo 7. Configure for DeepSeek 14B
echo 8. Exit
echo.
set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto CHECK_STATUS
if "%choice%"=="2" goto START_OLLAMA
if "%choice%"=="3" goto STOP_OLLAMA
if "%choice%"=="4" goto RESTART_OLLAMA
if "%choice%"=="5" goto TEST_API
if "%choice%"=="6" goto SHOW_MODELS
if "%choice%"=="7" goto CONFIGURE_14B
if "%choice%"=="8" goto EXIT
goto MENU

:CHECK_STATUS
echo.
echo 🔍 Checking Ollama Status...
echo.

REM Check if Ollama process is running
tasklist | findstr "ollama.exe" >nul 2>&1
if errorlevel 1 (
    echo ❌ Ollama service is NOT running
) else (
    echo ✅ Ollama service IS running
    echo.
    echo Running Ollama processes:
    tasklist | findstr "ollama"
)

echo.
REM Check if port 11434 is in use
netstat -an | findstr ":11434" >nul 2>&1
if errorlevel 1 (
    echo ❌ Port 11434 is NOT in use
) else (
    echo ✅ Port 11434 is in use (Ollama API active)
    echo.
    echo Port 11434 details:
    netstat -an | findstr ":11434"
)

echo.
pause
goto MENU

:START_OLLAMA
echo.
echo 🚀 Starting Ollama Service...

REM Check if already running
tasklist | findstr "ollama.exe" >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  Ollama is already running!
    echo Use option 4 to restart if needed.
    pause
    goto MENU
)

echo Starting Ollama in background...
start /min "Ollama Service" ollama serve

echo ⏳ Waiting 10 seconds for service to start...
timeout /t 10 /nobreak >nul

REM Verify it started
tasklist | findstr "ollama.exe" >nul 2>&1
if errorlevel 1 (
    echo ❌ Failed to start Ollama service
) else (
    echo ✅ Ollama service started successfully
)

echo.
pause
goto MENU

:STOP_OLLAMA
echo.
echo 🛑 Stopping Ollama Service...

REM Kill all Ollama processes
taskkill /f /im ollama.exe >nul 2>&1
if errorlevel 1 (
    echo ⚠️  No Ollama processes found to stop
) else (
    echo ✅ Ollama service stopped
)

echo ⏳ Waiting 3 seconds...
timeout /t 3 /nobreak >nul

REM Verify it stopped
tasklist | findstr "ollama.exe" >nul 2>&1
if errorlevel 1 (
    echo ✅ Ollama service fully stopped
) else (
    echo ⚠️  Some Ollama processes may still be running
)

echo.
pause
goto MENU

:RESTART_OLLAMA
echo.
echo 🔄 Restarting Ollama Service...

REM Stop first
echo Stopping existing service...
taskkill /f /im ollama.exe >nul 2>&1
timeout /t 5 /nobreak >nul

REM Start again
echo Starting service...
start /min "Ollama Service" ollama serve
timeout /t 10 /nobreak >nul

REM Verify
tasklist | findstr "ollama.exe" >nul 2>&1
if errorlevel 1 (
    echo ❌ Failed to restart Ollama service
) else (
    echo ✅ Ollama service restarted successfully
)

echo.
pause
goto MENU

:TEST_API
echo.
echo 🧪 Testing Ollama API Connection...

REM Test basic connection
echo Testing basic API connection...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ❌ Cannot connect to Ollama API
    echo Make sure Ollama is running (use option 2)
) else (
    echo ✅ API connection successful
    
    echo.
    echo API Response:
    curl -s http://localhost:11434/api/tags
)

echo.
pause
goto MENU

:SHOW_MODELS
echo.
echo 📋 Available Ollama Models...
echo.

REM Check if Ollama is running first
tasklist | findstr "ollama.exe" >nul 2>&1
if errorlevel 1 (
    echo ❌ Ollama service is not running
    echo Please start Ollama first (option 2)
) else (
    echo Available models:
    ollama list
)

echo.
pause
goto MENU

:CONFIGURE_14B
echo.
echo 🔧 Configuring for DeepSeek 14B...

REM First ensure Ollama is running
tasklist | findstr "ollama.exe" >nul 2>&1
if errorlevel 1 (
    echo Ollama not running - starting it first...
    start /min "Ollama Service" ollama serve
    timeout /t 10 /nobreak >nul
)

echo.
echo Available models:
ollama list

echo.
echo Looking for DeepSeek 14B model...
ollama list | findstr "14b" >nul 2>&1
if errorlevel 1 (
    echo ❌ No 14B model found
    echo Please check the model list above and ensure you have a 14B model installed.
    pause
    goto MENU
)

REM Get the exact model name
for /f "tokens=1" %%i in ('ollama list ^| findstr "14b"') do set model_name=%%i

echo ✅ Found model: %model_name%

REM Update .env file
echo.
echo Updating configuration...
(
echo # Ollama Configuration for DeepSeek 14B
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
) > .env

echo ✅ Configuration updated for: %model_name%

REM Test the model
echo.
echo Testing model...
echo print("Hello") | ollama run %model_name% >nul 2>&1
if errorlevel 1 (
    echo ❌ Model test failed
) else (
    echo ✅ Model is working correctly
)

echo.
pause
goto MENU

:EXIT
echo.
echo 👋 Exiting Ollama Service Manager
exit /b 0