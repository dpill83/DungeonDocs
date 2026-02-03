@echo off
rem Batch file to convert scraped D&D TXT files to Markdown for MkDocs, then build the site
cd /d "%~dp0"

echo Running the conversion script...
python scripts\txt_to_mkdocs.py

echo.
echo Building the site...
mkdocs build

echo.
echo Conversion and build finished!
echo Check the 'docs' folder for markdown and 'site' for the built site.
pause
