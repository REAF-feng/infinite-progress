@echo off
chcp 65001 >nul
echo ============================================
echo  MBTI Personality Test - Build EXE
echo ============================================
echo.
echo [1/3] Installing dependencies...
pip install matplotlib>=3.8.0 reportlab>=4.0.0 pyinstaller>=6.0
if errorlevel 1 (
    echo Failed! Check pip/network.
    pause
    exit /b 1
)
echo.
echo [2/3] Cleaning old build...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo.
echo [3/3] Building EXE...
pyinstaller ^
    --onedir ^
    --noconsole ^
    --name "MBTI_Test" ^
    --hidden-import matplotlib ^
    --hidden-import matplotlib.backends.backend_tkagg ^
    --hidden-import reportlab ^
    --hidden-import reportlab.pdfbase.ttfonts ^
    --collect-all matplotlib ^
    main.py
if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)
echo.
echo ============================================
echo  Build complete!
echo  Output: dist\MBTI_Test\MBTI_Test.exe
echo  Copy the entire MBTI_Test folder to any PC.
echo ============================================
pause
