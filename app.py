import os
import sys
import webbrowser
from threading import Timer
from flask import Flask, request, jsonify, render_template
from generate import convert_to_lithophane

app = Flask(__name__, template_folder="templates", static_folder="static")

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    uploaded_files = request.files.getlist("files")

    UPLOAD_DIR = "uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    results = []
    for f in uploaded_files:
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(0)
        results.append(f"{f.filename} — {size} bytes")
        
        filename = f.filename
        full_path = os.path.join(UPLOAD_DIR, filename)

        # Save file to server
        f.save(full_path)

        results.append(f"{filename} — {size} bytes")

        # Pass REAL path
        convert_to_lithophane(full_path)
    return jsonify({"result": "\n".join(results)})

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=False)
