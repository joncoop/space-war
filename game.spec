# -*- mode: python -*-

block_cipher = None


a = Analysis(['game.py'],
             pathex=['C:\\Users\\jccooper\\Desktop\\space-war-master'],
             binaries=[],
             datas=[('assets','assets')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Space War',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          icon = 'assets/images/app_icon.ico',
          version='version.txt')
