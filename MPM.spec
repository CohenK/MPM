# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['MPM.spec'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

a.datas += [('lock_and_key.png', 'C:\Users\cohen\OneDrive\Desktop\passMan\Resources\lock_and_key.png', 'Resources'),
            ('add.png', 'C:\Users\cohen\OneDrive\Desktop\passMan\Resources\add.png', 'Resources'),
            ('error.png', 'C:\Users\cohen\OneDrive\Desktop\passMan\Resources\error.png', 'Resources'),
            ('edit.png', 'C:\Users\cohen\OneDrive\Desktop\passMan\Resources\edit.png', 'Resources'),
            ('search.png', 'C:\Users\cohen\OneDrive\Desktop\passMan\Resources\search.png', 'Resources')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MPM',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MPM',
)
