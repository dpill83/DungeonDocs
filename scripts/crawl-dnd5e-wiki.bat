@echo off
REM Crawl and scrape the entire dnd5e.wikidot.com wiki into repo root scraped-dnd5e\
REM To re-run without overwriting existing files, use crawl-dnd5e-wiki-resume.bat
cd /d "%~dp0.."
python "%~dp0scrape_dnd_wiki.py" --crawl "https://dnd5e.wikidot.com/" -o scraped-dnd5e --delay 1
pause
