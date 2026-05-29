# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Exerset.
Builds standalone executables for Windows and Mac.
Usage:
  Windows: pyinstaller exerset.spec
  Mac:     pyinstaller exerset.spec
"""
import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=[str(Path.cwd()), str(Path.cwd() / 'src')],
    binaries=[],
    datas=[
        ('assets', 'assets'),
    ],
    hiddenimports=['PySide6', 'ctypes'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Exerset',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)

# For Mac: create app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='Exerset.app',
        icon='assets/icon.ico',
        bundle_identifier='com.exerset.deskworkerreset',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSHighResolutionCapable': 'True',
        },
    )
