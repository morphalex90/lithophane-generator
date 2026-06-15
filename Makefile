APP_NAME = lithophane-generator

# ----------------------------------------------------------------------------
# Local development (macOS / Linux)
# ----------------------------------------------------------------------------

# Create a dev virtualenv and install the runtime dependencies.
install:
	python3 -m venv venv
	./venv/bin/python -m pip install --upgrade pip
	./venv/bin/python -m pip install -r requirements.txt

# Run the app locally. Serves on http://127.0.0.1:5000 and opens the browser.
run:
	./venv/bin/python app.py

# ----------------------------------------------------------------------------
# Packaging
#
# Builds run from an ISOLATED venv (buildvenv) that contains ONLY the real
# dependencies plus PyInstaller. Building from a global / Anaconda environment
# sweeps in unrelated libraries (torch, cv2, ...) and bloats the binary to
# 600+ MB; the clean venv keeps it around ~45 MB.
#
# PyInstaller cannot cross-compile: build the macOS binary ON macOS and the
# Windows .exe ON Windows.
# ----------------------------------------------------------------------------

# Build the macOS executable -> dist/lithophane-generator
build-macos:
	python3 -m venv buildvenv
	./buildvenv/bin/python -m pip install --upgrade pip
	./buildvenv/bin/python -m pip install -r requirements.txt pyinstaller
	rm -rf build dist/$(APP_NAME)
	./buildvenv/bin/pyinstaller --noconfirm lithophane-generator.spec
	@echo "macOS build ready: dist/$(APP_NAME)"

# Build the Windows executable -> dist\lithophane-generator.exe  (must be run ON Windows)
build-windows:
	python -m venv buildvenv
	buildvenv\Scripts\python -m pip install --upgrade pip
	buildvenv\Scripts\python -m pip install -r requirements.txt pyinstaller
	buildvenv\Scripts\pyinstaller --noconfirm lithophane-generator.spec
	@echo Windows build ready: dist\lithophane-generator.exe

# Remove build artifacts and the isolated build venv.
clean:
	rm -rf build dist buildvenv __pycache__

.PHONY: install run build-macos build-windows clean
