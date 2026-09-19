# -*- mode: python ; coding: utf-8 -*-
"""
Spec de PyInstaller para empaquetar la GUI de Hipoteca Inversa (Kivy) en un
ejecutable de Windows.

Uso (desde la raíz del proyecto, con el venv activado):
    python -m PyInstaller HipotecaInversa.spec --clean

El .exe queda en dist\\HipotecaInversa\\HipotecaInversa.exe
"""

from kivy_deps import sdl2, glew, angle

block_cipher = None

a = Analysis(
    ["src/view/gui/hipoteca_inversa_gui.py"],
    pathex=["."],
    binaries=[],
    datas=[],
    hiddenimports=[
        "src.model.logica_hipoteca_inversa",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="HipotecaInversa",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,          # False = sin ventana negra de consola detrás de la GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="assets/HipotecaInversa_logo.ico", 
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins + angle.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name="HipotecaInversa",
)
