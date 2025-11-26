# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['work_time.py'],
    pathex=[],
    binaries=[],
    datas=[('font\\*', 'font'), ('liver.ico', '.')],  # 若程式不需在執行時讀 liver.ico，這行就不放 liver.ico,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2, # 等同 PYTHONOPTIMIZE=2：移除 assert/docstring
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,   # one-file：把 binaries/zipfiles/datas 都加進來
    a.zipfiles,
    a.datas,
    [],
    exclude_binaries=False,
    name='work_time_one',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,     # 可小幅減少大小
    upx=True,      # 關閉 UPX，避免誤報與啟動延遲
    console=False,  # GUI 程式關閉主控台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='liver.ico' , # 如需圖示：'icon.ico'
)

