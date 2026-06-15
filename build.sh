#!/bin/bash
# --- Customize these variables ---
APP_NAME="MyCoolApp"
ICON_PATH="path/to/icon.icns"

# --- Run PyInstaller ---
pyinstaller --onefile --name "$APP_NAME" --icon "$ICON_PATH" --add-data "templates:templates" --add-data "static:static" app.py

echo "Build complete! Executable is in the dist/ folder."
