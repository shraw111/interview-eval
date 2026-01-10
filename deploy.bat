@echo off
REM Deploy to Azure - Wrapper script that ensures Azure CLI is in PATH

REM Add Azure CLI to PATH for this session
set PATH=%PATH%;C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin

REM Run the PowerShell deployment script
powershell -ExecutionPolicy Bypass -File "%~dp0deploy-azure.ps1"

pause
