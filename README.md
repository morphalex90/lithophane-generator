# Pet Cemetery Lithophane

A small Flask web app that turns an uploaded image into a 3D-printable
lithophane. For each image it generates two STL files next to the uploaded
file in the `uploads/` directory:

- `<name>_Flat.stl` — a flat lithophane plate
- `<name>_Cylinder.stl` — the same lithophane wrapped into a cylinder

## Requirements

- Python 3.9+
- The packages listed in [requirements.txt](requirements.txt) (`lithophane`, `Flask`)

## Run locally

### 1. Clone and enter the project

    git clone https://github.com/<your-account>/pet-cemetery-lithophane.git
    cd pet-cemetery-lithophane

### 2. Create and activate a virtual environment (recommended)

macOS / Linux:

    python3 -m venv venv
    source venv/bin/activate

Windows (PowerShell):

    python -m venv venv
    venv\Scripts\Activate.ps1

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Start the app

    python app.py

The server starts on http://127.0.0.1:5000 and your default browser opens
automatically. Use the page to upload one or more images; the generated STL
files appear in the `uploads/` folder.

> Tip: the app uses a headless (non-GUI) matplotlib backend, so it runs fine
> on servers and over SSH without a display.

## To build into an application

### Windows

    pyinstaller --onefile --name MyCoolApp --icon path/to/icon.ico --add-data "templates;templates" --add-data "static;static" app.py

### macOS/Linux

    pyinstaller --onefile --name MyCoolApp --icon path/to/icon.icns --add-data "templates:templates" --add-data "static:static" app.py

Otherwise use `build.bat` for Windows and `build.sh` for macOS (remember to
`chmod +x build.sh`).
