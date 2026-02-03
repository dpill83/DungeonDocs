@echo off
rem Start MkDocs dev server so you can view DungeonDocs at http://127.0.0.1:8000
cd /d "%~dp0"

echo Starting MkDocs server...
echo Open http://127.0.0.1:8000 in your browser.
echo Press Ctrl+C to stop.
echo.
mkdocs serve
