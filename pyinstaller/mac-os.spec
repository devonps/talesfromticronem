# -*- mode: python -*-

block_cipher = None

added_files = [('../static', 'static')]

a = Analysis(['../ticronem.py'],
             binaries=[],
             datas = added_files,
             hiddenimports=['bearlibterminal'],
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
          [],
          name='ticronem',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False)
app = BUNDLE(exe,
             name='ticronem.app',
             icon=None,
             bundle_identifier=None)
