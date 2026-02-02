@echo off
echo ========================================
echo Starting Task Manager Application
echo ========================================
echo.
echo [1/2] Starting Backend Server...
cd backend
start "Task Manager Backend" cmd /k "python -m uvicorn main:app --reload"
echo.
echo [2/2] Waiting for server to start...
timeout /t 3 /nobreak > nul
echo.
echo Opening Application in Browser...
cd ..
echo start by clicking on the link
echo chrome "http://localhost:63342/API_Taskmanager/frontend/home.html"
echo.
echo ========================================
echo Application Started!
echo ========================================
echo Backend Server: http://localhost:8000
echo Frontend: Check your browser
echo.
echo To stop the server, close the backend window
echo ========================================
pause