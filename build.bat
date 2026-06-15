@echo off
REM --- Customize these variables ---
set APP_NAME=MyCoolApp
set ICON_PATH=path\to\icon.ico

REM --- Run PyInstaller ---
pyinstaller --onefile --name %APP_NAME% --icon %ICON_PATH% --add-data "templates;templates" --add-data "static;static" app.py

echo.
echo Build complete! Executable is in the dist\ folder.
pause
