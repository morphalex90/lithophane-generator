# Lithophane Generator

A small Flask web app that turns an uploaded image into a 3D-printable
lithophane. For each image it generates two STL files next to the uploaded
file in the `uploads/` directory:

- `<name>_Flat.stl` — a flat lithophane plate
- `<name>_Cylinder.stl` — the same lithophane wrapped into a cylinder

## Download

Grab a prebuilt standalone app — no Python setup required:

- **macOS:** [Download for macOS](https://github.com/morphalex90/lithophane-generator/releases/latest/download/MyCoolApp-macos)
- **Windows:** [Download for Windows](https://github.com/morphalex90/lithophane-generator/releases/latest/download/MyCoolApp-windows.exe)

These always point at the newest build, published automatically from
[GitHub Actions](.github/workflows/build.yml) on every update to `main`.

Prefer to run from source or build it yourself? See [Run locally](#run-locally) and
[Build a standalone application](#build-a-standalone-application) below.

## Requirements

- Python 3.9+
- The packages listed in [requirements.txt](requirements.txt) (`lithophane`, `Flask`)

## Run locally

The quickest path on macOS / Linux is the `Makefile`:

    git clone https://github.com/morphalex90/lithophane-generator.git
    cd lithophane-generator
    make install      # create the venv and install dependencies
    make run          # start the app

The server starts on http://127.0.0.1:5000 and your default browser opens
automatically. Use the page to upload one or more images; the generated STL
files appear in the `uploads/` folder.

> Tip: the app uses a headless (non-GUI) matplotlib backend, so it runs fine
> on servers and over SSH without a display.

<details>
<summary>Manual setup (or Windows)</summary>

Create and activate a virtual environment:

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate

    # Windows (PowerShell)
    python -m venv venv
    venv\Scripts\Activate.ps1

Install dependencies and start the app:

    pip install -r requirements.txt
    python app.py

</details>

## Build a standalone application

Builds are produced with [PyInstaller](https://pyinstaller.org/) from an
**isolated virtualenv** that holds only the real dependencies. Building from a
global or Anaconda environment sweeps in unrelated libraries (torch, OpenCV,
...) and bloats the binary to 600+ MB; the clean venv keeps it small. The
`Makefile` and [MyCoolApp.spec](MyCoolApp.spec) handle this for you.

> PyInstaller cannot cross-compile: build the macOS binary on macOS and the
> Windows `.exe` on Windows.

### macOS

    make build-macos          # -> dist/MyCoolApp

### Windows

    make build-windows         # -> dist\MyCoolApp.exe

If `make` is not available on Windows, run the same steps by hand:

    python -m venv buildvenv
    buildvenv\Scripts\python -m pip install -r requirements.txt pyinstaller
    buildvenv\Scripts\pyinstaller --noconfirm MyCoolApp.spec

(`build.sh` / `build.bat` remain as thin wrappers around the same commands;
remember to `chmod +x build.sh` on macOS.)

### Clean up build artifacts

    make clean
