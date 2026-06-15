import os
import sys
import time
import webbrowser
from threading import Timer
from flask import Flask, request, jsonify, render_template, send_from_directory, url_for
from werkzeug.utils import secure_filename
from generate import convert_to_lithophane

# Unique per process. Each reloader restart re-imports this module and gets a
# new value, which the dev live-reload client uses to detect a restart.
SERVER_ID = str(time.time())

FROZEN = getattr(sys, "frozen", False)

def resource_path(relative_path):
    # When frozen by PyInstaller, bundled data (templates/static) lives in the
    # temporary _MEIPASS dir, not next to the cwd. Resolve against it.
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

app = Flask(
    __name__,
    template_folder=resource_path("templates"),
    static_folder=resource_path("static"),
)

# Re-render templates on every request without restarting (dev convenience).
app.config["TEMPLATES_AUTO_RELOAD"] = True

def output_dir():
    """Directory holding uploaded images and the STL files we generate.

    It must be user-writable. A frozen app bundle is read-only (and signed on
    macOS), and it's launched with an unpredictable working directory, so a
    relative "uploads" path would fail there. We therefore write under the
    user's home when frozen, and keep a local ./uploads from source for dev."""
    if getattr(sys, "frozen", False):
        base = os.path.join(os.path.expanduser("~"), "LithophaneGenerator")
    else:
        base = os.path.join(os.path.abspath("."), "uploads")
    os.makedirs(base, exist_ok=True)
    return base

@app.route("/")
def index():
    # Only wire up live-reload polling in dev; the frozen app never restarts.
    return render_template("index.html", live_reload=not FROZEN)

@app.route("/livereload")
def livereload():
    return jsonify({"id": SERVER_ID})

@app.route("/process", methods=["POST"])
def process():
    uploaded_files = request.files.getlist("files")

    # Which lithophane variant(s) to generate: "flat", "cylinder" or "both".
    shape = request.form.get("shape", "both")
    if shape not in ("flat", "cylinder", "both"):
        return jsonify({"error": f"Invalid shape: {shape}"}), 400

    # Numeric generation parameters (defaults mirror convert_to_lithophane).
    try:
        width = float(request.form.get("width", 102))
        depth = float(request.form.get("depth", 3))
        offset = float(request.form.get("offset", 0.5))
    except ValueError:
        return jsonify({"error": "Width, depth and offset must be numbers."}), 400

    if width <= 0 or depth <= 0 or offset < 0:
        return jsonify({"error": "Width and depth must be > 0, offset >= 0."}), 400

    upload_dir = output_dir()

    items = []
    for f in uploaded_files:
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(0)

        # Sanitize the client-supplied filename to prevent path traversal.
        filename = secure_filename(f.filename)
        if not filename:
            continue
        full_path = os.path.join(upload_dir, filename)

        # Save file to server
        f.save(full_path)

        # Pass REAL path
        outputs = convert_to_lithophane(
            full_path, shape=shape, width=width, depth=depth, offset=offset
        )

        items.append({
            "source": filename,
            "size": size,
            "files": [
                {
                    "name": os.path.basename(p),
                    "url": url_for("download", filename=os.path.basename(p)),
                }
                for p in outputs
            ],
        })
    return jsonify({"items": items})

@app.route("/files/<path:filename>")
def download(filename):
    # send_from_directory rejects paths that escape the directory, so a
    # crafted filename can't reach files outside the output folder.
    return send_from_directory(output_dir(), filename, as_attachment=True)

# Port can be overridden via the PORT env var. Handy when something else on the
# machine already holds 5000 (e.g. macOS AirPlay Receiver / Control Center).
PORT = int(os.environ.get("PORT", "5000"))

def open_browser():
    webbrowser.open(f"http://127.0.0.1:{PORT}")

def watched_files():
    """Extra files (templates, static assets) that should trigger a reload
    when edited, in addition to the .py files Werkzeug watches by default."""
    extra = []
    for folder in ("templates", "static"):
        for root, _, files in os.walk(folder):
            extra.extend(os.path.join(root, f) for f in files)
    return extra

if __name__ == "__main__":
    # Open the browser exactly once, on first launch. The reloader restarts the
    # *worker* (WERKZEUG_RUN_MAIN == "true") on every edit, so opening there
    # would spawn a new tab each time. The supervisor process (where the var is
    # unset) starts only once, so we open there instead. When frozen there's no
    # reloader and the var is also unset, so this covers that case too. On
    # reload the open tab refreshes itself via /livereload (see livereload.js).
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        Timer(1, open_browser).start()

    # Auto-reload on edits during development. Disabled in a PyInstaller build,
    # where the reloader can't relaunch the frozen interpreter.
    app.run(
        port=PORT,
        debug=not FROZEN,
        use_reloader=not FROZEN,
        extra_files=watched_files(),
    )
