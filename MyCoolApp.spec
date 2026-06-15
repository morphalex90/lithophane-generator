# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# scikit-image (pulled in by lithophane) exposes its API through `lazy_loader`,
# which resolves names like `skimage.transform.resize` at runtime from the
# package's `__init__.pyi` stub files. PyInstaller doesn't collect those stubs
# or the lazily-imported submodules by default, so the frozen app fails with
# "cannot import name 'resize' from 'skimage.transform'". Collect them explicitly.
skimage_hiddenimports = collect_submodules('skimage')
skimage_datas = collect_data_files('skimage', includes=['**/*.pyi'])


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('templates', 'templates'), ('static', 'static')] + skimage_datas,
    hiddenimports=skimage_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Heavy libs the app never uses; excluded defensively so nothing
        # transitively drags them into the bundle.
        'torch', 'tensorflow', 'cv2', 'transformers', 'plotly', 'pandas',
        'sympy', 'gradio', 'panel', 'bokeh', 'statsmodels', 'sklearn',
        'onnxruntime', 'diffusers', 'gensim', 'astropy', 'spyder',
        # matplotlib runs headless (Agg) - drop GUI backends and dev tooling.
        'tkinter', 'PyQt5', 'PyQt6', 'PySide2', 'PySide6', 'wx',
        'IPython', 'jupyter', 'notebook', 'pytest',
    ],
    noarchive=False,
    # Keep optimize=0. Building with -OO (optimize=2) breaks scikit-image's
    # lazy_loader stub resolution at runtime, so `from skimage.transform import
    # resize` fails inside the frozen app ("cannot import name 'resize'").
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MyCoolApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/icon.icns', 'assets/icon.ico'],
)
