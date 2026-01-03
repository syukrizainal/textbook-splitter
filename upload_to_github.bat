@echo off
echo ============================================================
echo GitHub Upload Helper
echo ============================================================
echo.

set /p USERNAME="Enter your GitHub username: "
set /p EMAIL="Enter your GitHub email: "
set /p REPO="Enter repository name [cfa-l2-pdf-splitter]: "

if "%REPO%"=="" set REPO=cfa-l2-pdf-splitter

echo.
echo ============================================================
echo Step 1: Configure Git
echo ============================================================
git config --global user.name "%USERNAME%"
git config --global user.email "%EMAIL%"
echo Git configured
echo.

echo ============================================================
echo Step 2: Initialize Git Repository
echo ============================================================
cd /d "%~dp0"
git init
echo Git initialized
echo.

echo ============================================================
echo Step 3: Create README.md
echo ============================================================
echo # %REPO% > README.md
echo. >> README.md
echo Python scripts to split CFA Level 2 textbooks. >> README.md
echo. >> README.md
echo ## Usage >> README.md
echo pip install pypdf >> README.md
echo python split_pdf_by_reading.py "path/to/pdf" >> README.md
echo README.md created
echo.

echo ============================================================
echo Step 4: Add and Commit Files
echo ============================================================
git add .
git commit -m "Initial commit: CFA Level 2 PDF splitter"
echo Files committed
echo.

echo ============================================================
echo Step 5: Create GitHub Repository
echo ============================================================
echo.
echo Please follow these steps:
echo.
echo 1. Open your browser and go to: https://github.com/new
echo 2. Repository name: %REPO%
echo 3. Make it Public
echo 4. Click 'Create repository'
echo 5. Come back here and press any key to continue
echo.

pause

echo.
echo Pushing to GitHub...
git remote add origin https://github.com/%USERNAME%/%REPO%.git
git branch -M main
git push -u origin main

echo.
echo ============================================================
echo DONE!
echo ============================================================
echo.
echo Your repository is at: https://github.com/%USERNAME%/%REPO%
echo.
pause
