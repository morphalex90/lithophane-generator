## To build into an application:

### Windows
    pyinstaller --onefile --name MyCoolApp --icon path/to/icon.ico --add-data "templates;templates" --add-data "static;static" app.py

### macOS/Linux
    pyinstaller --onefile --name MyCoolApp --icon path/to/icon.icns --add-data "templates:templates" --add-data "static:static" app.py

Otherwise use build.bat for Windows and build.sh for MacOS (remember to `chmod +x build.sh`)