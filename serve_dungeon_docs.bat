@echo off
cls
rem Start MkDocs dev server so you can view DungeonDocs at http://127.0.0.1:8000
cd /d "%~dp0"

rem Free port 8000 if something is still listening (e.g. previous run)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /PID %%a /F >nul 2>&1

echo Starting MkDocs server...
echo Open http://127.0.0.1:8000 in your browser.
echo.
echo Leave this window open. Changes to docs or CSS will auto-refresh in your browser.
echo Press Ctrl+C to stop.
echo.
mkdocs serve --livereload --watch-theme
