# Configurações do Jogo Super Hero
import pygame

# Configurações da tela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Configurações do mundo
WORLD_WIDTH = 3840
WORLD_HEIGHT = 720

# Configurações dos personagens (melhor proporção)
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 96
ENEMY_WIDTH = 60
ENEMY_HEIGHT = 90
COIN_SIZE = 32

# ===== FÍSICA OTIMIZADA =====
GRAVITY = 0.8
MAX_FALL_SPEED = 12
JUMP_STRENGTH = -15
PLAYER_SPEED = 5
ENEMY_SPEED = 2

# Configurações de colisão simplificadas
PLATFORM_SNAP_DISTANCE = 10
COLLISION_TOLERANCE = 2

# ===== CONFIGURAÇÕES DE JOGO =====

PLAYER_MAX_HEALTH = 100
PLAYER_ATTACK_DAMAGE = 25
ENEMY_MAX_HEALTH = 50
COIN_VALUE = 10
POWERUP_COIN_VALUE = 50
BONUS_COIN_VALUE = 20

# Configurações de tempo
LEVEL_TIME = 300  # 5 minutos por nível
BONUS_COIN_DURATION = 10  # segundos

# Configurações da interface
HUD_HEIGHT = 80
HUD_MARGIN = 20
HUD_FONT_SIZE = 28
TEXT_FONT_SIZE = 22

# Configurações da câmera
CAMERA_SPEED = 0.1
CAMERA_BORDER = 200

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
LIME = (0, 255, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
SKY_BLUE = (135, 206, 235)

# Cores da interface
UI_BG_COLOR = (0, 0, 0, 180)
UI_BORDER_COLOR = WHITE
UI_TEXT_COLOR = WHITE
UI_ACCENT_COLOR = GOLD
UI_HEALTH_COLOR = RED

# Dimensões das plataformas
PLATFORM_HEIGHT = 32
GROUND_HEIGHT = 80

# Configurações de jogo
INITIAL_LIVES = 3
INVULNERABILITY_TIME = 120  # 2 segundos a 60 FPS

# Estados do jogo
GAME_MENU = 0
GAME_PLAYING = 1
GAME_PAUSED = 2
GAME_OVER = 3
GAME_COMPLETE = 4

# Caminhos dos arquivos
ASSETS_PATH = "assets/"
IMAGES_PATH = ASSETS_PATH + "images/"
SOUNDS_PATH = ASSETS_PATH + "sounds/"

# Imagens
PLAYER_IMAGE = IMAGES_PATH + "pparado.png"
ENEMY_IMAGE = IMAGES_PATH + "vparado.png"
COIN_IMAGE = IMAGES_PATH + "coin.png"
PLATFORM_IMAGE = IMAGES_PATH + "platform.png"
BACKGROUND_IMAGE = IMAGES_PATH + "cenario.jpg"

# Sons
COIN_SOUND = SOUNDS_PATH + "coin.wav"
JUMP_SOUND = SOUNDS_PATH + "jump.wav"
ATTACK_SOUND = SOUNDS_PATH + "attack.wav"
GAME_OVER_SOUND = SOUNDS_PATH + "game_over.wav"

# Configurações de animação
ANIMATION_SPEED = 8  # Frames por animação
IDLE_ANIMATION_SPEED = 30  # Animação idle mais lenta

# Configurações da interface
HUD_HEIGHT = 100
HUD_MARGIN = 20
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
MENU_FONT_SIZE = 64
HUD_FONT_SIZE = 32
TEXT_FONT_SIZE = 24

# Configurações de efeitos visuais
PARTICLE_COUNT = 10
EFFECT_DURATION = 60
GLOW_INTENSITY = 50

# Configurações da câmera
CAMERA_SMOOTHING = 0.1
CAMERA_DEADZONE = 200

# Configurações dos inimigos
ENEMY_PATROL_DISTANCE = 200

# Configurações das moedas
COIN_ANIMATION_SPEED = 8

# Configurações do jogo
RESPAWN_INVULNERABILITY_TIME = 120  # frames

# Configurações da câmera
WORLD_WIDTH = SCREEN_WIDTH * 4  # Mundo 4x maior que a tela
WORLD_HEIGHT = SCREEN_HEIGHT

# Caminhos dos assets
ASSETS_PATH = 'assets/'
IMAGES_PATH = ASSETS_PATH + 'images/'
SOUNDS_PATH = ASSETS_PATH + 'sounds/'

# Sons
JUMP_SOUND = SOUNDS_PATH + 'jump.mp3'
COIN_SOUND = SOUNDS_PATH + 'coin.mp3'
GAME_OVER_SOUND = SOUNDS_PATH + 'game-over.mp3'

# Imagens
BACKGROUND_IMAGE = IMAGES_PATH + 'cenario.jpg'
COIN_IMAGE = IMAGES_PATH + 'coin.png'

# Imagens do jogador
PLAYER_IDLE = IMAGES_PATH + "pparado.png"      # Jogador parado
PLAYER_WALK = IMAGES_PATH + "pandando.png"     # Jogador andando  
PLAYER_JUMP = IMAGES_PATH + "ppulando.png"     # Jogador pulando
PLAYER_ATTACK = IMAGES_PATH + "patacando.png"  # Jogador atacando

# Imagens dos inimigos
ENEMY_IDLE = IMAGES_PATH + "vparado.png"       # Inimigo parado
ENEMY_WALK = IMAGES_PATH + "vandando.png"      # Inimigo andando
ENEMY_ATTACK = IMAGES_PATH + "vatacando.png"   # Inimigo atacando
ENEMY_HIT = IMAGES_PATH + "vsofrendo.png"      # Inimigo sofrendo dano

# Estados do jogo
GAME_PLAYING = 0
GAME_PAUSED = 1
GAME_OVER = 2
GAME_MENU = 3 