# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),  # Inclui toda a pasta assets
        ('game', 'game'),      # Inclui todo o módulo game
    ],
    hiddenimports=[
        'pygame',
        'pygame.mixer',
        'pygame.font',
        'pygame.image',
        'pygame.transform',
        'pygame.sprite',
        'pygame.surface',
        'pygame.rect',
        'pygame.display',
        'pygame.event',
        'pygame.key',
        'pygame.time',
        'pygame.draw',
        'game.settings',
        'game.utils',
        'game.player',
        'game.enemy',
        'game.coin',
        'game.platform',
        'game.game_manager',
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SuperHero',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Não mostra console no Windows
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Você pode adicionar um ícone aqui se tiver
)

# Para macOS, criar um app bundle
app = BUNDLE(
    exe,
    name='SuperHero.app',
    icon=None,
    bundle_identifier='com.superhero.game',
    info_plist={
        'CFBundleName': 'Super Hero',
        'CFBundleDisplayName': 'Super Hero - Jogo de Plataforma',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
    },
) 