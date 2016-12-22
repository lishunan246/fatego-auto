# -*- mode: python -*-
# coding=utf-8
block_cipher = None

added_files = [
         ( 'image', 'image' ),
         ( 'LICENSE.md', '.' ),
         ( 'README.md', '.' ),
         ( 'target.png', '.'),
         ('icon.ico','.')
         ]

a = Analysis(['main.pyw'],
             pathex=[],
             binaries=None,
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='zhuazi',
          debug=False,
          strip=False,
          upx=True,
          icon='icon.ico',
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,

               name='ZhuaZi')
