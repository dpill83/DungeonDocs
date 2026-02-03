@echo off
REM Kill anything already listening on 8123 (ignore errors)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8123 ^| findstr LISTENING') do taskkill /PID %%a /F >nul 2>&1
mkdocs serve -a 127.0.0.1:8123
