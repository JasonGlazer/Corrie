# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['runner.py'],
             pathex=['C:\\Users\\jglaz\\Documents\\projects\\SBIR SimArchImag\\5 SimpleBox\\corrie\\corrie'],
             binaries=[],
             datas=[('seed', 'seed'), ('measures', 'measures'), ("C:/Users/jglaz/AppData/Roaming/Python/Python37/site-packages/pptx/templates", "pptx/templates")],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='corrie',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='corrie')
