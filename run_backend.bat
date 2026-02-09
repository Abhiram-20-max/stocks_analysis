@echo off
echo Starting Backend...
set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
if not exist "%PYTHON_EXE%" (
	echo Python venv not found at %PYTHON_EXE%
	echo Create it first or adjust this path.
	exit /b 1
)
cd /d "%~dp0backend"
"%PYTHON_EXE%" run.py
pause
