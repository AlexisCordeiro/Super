import pygame
import random
import sys
from game.utils import load_image, draw_text, draw_text_left, draw_text_right, Camera, clamp, draw_gradient_rect, load_sound
from game.settings import *
from game.player import Player
from game.enemy import Enemy
from game.coin import Coin, PowerUpCoin, BonusCoin
from game.platform import Platform, MovingPlatform, DisappearingPlatform, BouncePlatform

class GameManager:
    """Gerenciador principal do jogo"""
    
    def __init__(self):
        # Inicialização do Pygame
        pygame.init()
        pygame.mixer.init()
        
        # Tela
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Hero - Jogo de Plataforma")
        self.clock = pygame.time.Clock()
        
        # Estado do jogo
        self.game_state = GAME_MENU
        self.running = True
        
        # Sistema de câmera
        self.camera = Camera(WORLD_WIDTH, WORLD_HEIGHT)
        
        # Controle de tela
        self.screen_shake = 0
        
        # Fontes
        self.font_large = pygame.font.Font(None, MENU_FONT_SIZE)
        self.font_medium = pygame.font.Font(None, HUD_FONT_SIZE)
        self.font_small = pygame.font.Font(None, TEXT_FONT_SIZE)
        
        # Background
        self.background = None
        self.load_background()
        
        # Sons
        self.load_sounds()
        
        # Variáveis do jogo
        self.score = 0
        self.level = 1
        self.max_level = 2  # Apenas 2 fases
        self.lives = INITIAL_LIVES
        self.time_remaining = 300  # 5 minutos
        self.game_timer = 0
        
        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        
        # Player
        self.player = None
        
        # Interface
        self.menu_selection = 0
        self.menu_options = ["JOGAR", "SAIR"]
        self.pause_selection = 0
        self.pause_options = ["CONTINUAR", "MENU", "SAIR"]
        
        # Efeitos visuais
        self.fade_alpha = 0
        self.transition_timer = 0
        
        # Estatísticas
        self.coins_collected = 0
        self.enemies_defeated = 0
        self.best_score = 0
        
    def load_background(self):
        """Carrega imagem de fundo sem esticar"""
        try:
            # Carrega a imagem original
            original_bg = load_image(BACKGROUND_IMAGE)
            original_width = original_bg.get_width()
            original_height = original_bg.get_height()
            
            print(f"📸 Imagem de fundo original: {original_width}x{original_height}px")
            
            # Calcula escala mantendo proporção
            scale_x = WORLD_WIDTH / original_width
            scale_y = WORLD_HEIGHT / original_height
            scale = min(scale_x, scale_y)  # Usa menor escala para não esticar
            
            # Redimensiona mantendo proporção
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
            scaled_bg = pygame.transform.scale(original_bg, (new_width, new_height))
            
            print(f"📸 Imagem redimensionada: {new_width}x{new_height}px (escala: {scale:.2f})")
            
            # Cria superfície do mundo
            self.background = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
            
            # Se a imagem for menor que o mundo, repete ela
            if new_width < WORLD_WIDTH or new_height < WORLD_HEIGHT:
                print("🔄 Repetindo imagem de fundo para preencher o mundo...")
                
                # Preenche com cor de céu primeiro
                self.background.fill(SKY_BLUE)
                
                # Repete a imagem horizontalmente e verticalmente
                for x in range(0, WORLD_WIDTH, new_width):
                    for y in range(0, WORLD_HEIGHT, new_height):
                        # Calcula área a ser copiada
                        copy_width = min(new_width, WORLD_WIDTH - x)
                        copy_height = min(new_height, WORLD_HEIGHT - y)
                        
                        if copy_width > 0 and copy_height > 0:
                            # Cria subsuperfície se necessário
                            if copy_width == new_width and copy_height == new_height:
                                self.background.blit(scaled_bg, (x, y))
                            else:
                                sub_surface = pygame.Surface((copy_width, copy_height))
                                sub_surface.blit(scaled_bg, (0, 0))
                                self.background.blit(sub_surface, (x, y))
            else:
                # Se a imagem é maior ou igual, apenas centraliza
                offset_x = (WORLD_WIDTH - new_width) // 2
                offset_y = (WORLD_HEIGHT - new_height) // 2
                self.background.fill(SKY_BLUE)
                self.background.blit(scaled_bg, (offset_x, offset_y))
            
            print("✅ Fundo carregado com sucesso!")
            
        except Exception as e:
            print(f"⚠️ Erro ao carregar fundo: {e}")
            # Cria um fundo gradiente se não conseguir carregar
            self.background = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
            draw_gradient_rect(self.background, 
                             pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT),
                             SKY_BLUE, (135, 206, 250))
            print("🎨 Usando fundo gradiente como fallback")
    
    def load_sounds(self):
        """Carrega sons do jogo"""
        try:
            self.coin_sound = load_sound(COIN_SOUND, 0.5)
            self.game_over_sound = load_sound(GAME_OVER_SOUND, 0.7)
        except:
            self.coin_sound = None
            self.game_over_sound = None
    
    def create_level(self, level_num):
        """Cria um nível específico"""
        # Limpa sprites existentes
        self.all_sprites.empty()
        self.platforms.empty()
        self.enemies.empty()
        self.coins.empty()
        
        if level_num == 1:
            self.create_level_1()
        elif level_num == 2:
            self.create_level_2()
        
        # Cria o player
        self.player = Player(100, SCREEN_HEIGHT - 200, self.platforms)
        self.all_sprites.add(self.player)

    def create_level_1(self):
        """Cria o primeiro nível - Tutorial e introdução"""
        print("🎮 Criando Nível 1 - Tutorial")
        
        # Plataformas básicas - tutorial de movimento (espaçamentos melhorados)
        platforms_data = [
            # Plataformas iniciais (tutorial)
            (0, SCREEN_HEIGHT - 100, 300, 40, "grass"),      # Plataforma inicial
            (350, SCREEN_HEIGHT - 150, 200, 40, "normal"),   # Primeira elevação (reduzido de 400 para 350)
            (600, SCREEN_HEIGHT - 200, 180, 40, "wood"),     # Segunda elevação (reduzido de 700 para 600)
            (830, SCREEN_HEIGHT - 120, 150, 40, "stone"),    # Descida (reduzido de 950 para 830)
            
            # Seção de saltos básicos
            (1030, SCREEN_HEIGHT - 180, 120, 40, "normal"),  # Salto médio (reduzido de 1200 para 1030)
            (1200, SCREEN_HEIGHT - 240, 100, 40, "wood"),    # Salto alto (reduzido de 1400 para 1200)
            (1350, SCREEN_HEIGHT - 180, 120, 40, "grass"),   # Descida (reduzido de 1600 para 1350)
            (1520, SCREEN_HEIGHT - 120, 200, 40, "stone"),   # Plataforma larga (reduzido de 1800 para 1520)
            
            # Seção de plataformas especiais
            (1770, SCREEN_HEIGHT - 200, 80, 40, "cloud"),    # Plataforma nuvem (reduzido de 2100 para 1770)
            (1900, SCREEN_HEIGHT - 280, 80, 40, "ice"),      # Plataforma gelo (reduzido de 2250 para 1900)
            (2030, SCREEN_HEIGHT - 200, 100, 40, "bounce"),  # Plataforma de impulso (reduzido de 2400 para 2030)
            (2180, SCREEN_HEIGHT - 300, 120, 40, "wood"),    # Plataforma alta (reduzido de 2600 para 2180)
            
            # Final do nível
            (2350, SCREEN_HEIGHT - 160, 300, 40, "grass"),   # Plataforma final (reduzido de 2800 para 2350)
            (2700, SCREEN_HEIGHT - 200, 200, 40, "stone"),   # Última plataforma (reduzido de 3200 para 2700)
        ]
        
        # Cria plataformas
        for x, y, width, height, platform_type in platforms_data:
            if platform_type == "bounce":
                platform = BouncePlatform(x, y, width, height)
            else:
                platform = Platform(x, y, width, height, platform_type)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
        
        # Moedas do nível 1 (ajustadas para novas posições)
        coin_positions = [
            (400, SCREEN_HEIGHT - 200, "normal"),    # Ajustado de 450 para 400
            (650, SCREEN_HEIGHT - 250, "bonus"),     # Ajustado de 750 para 650
            (880, SCREEN_HEIGHT - 170, "normal"),    # Ajustado de 1000 para 880
            (1080, SCREEN_HEIGHT - 230, "special"),  # Ajustado de 1250 para 1080
            (1250, SCREEN_HEIGHT - 290, "bonus"),    # Ajustado de 1450 para 1250
            (1400, SCREEN_HEIGHT - 230, "normal"),   # Ajustado de 1660 para 1400
            (1570, SCREEN_HEIGHT - 170, "normal"),   # Ajustado de 1900 para 1570
            (1820, SCREEN_HEIGHT - 250, "bonus"),    # Ajustado de 2150 para 1820
            (1950, SCREEN_HEIGHT - 330, "special"),  # Ajustado de 2300 para 1950
            (2080, SCREEN_HEIGHT - 250, "normal"),   # Ajustado de 2450 para 2080
            (2230, SCREEN_HEIGHT - 350, "bonus"),    # Ajustado de 2660 para 2230
            (2400, SCREEN_HEIGHT - 210, "special"),  # Ajustado de 2900 para 2400
            (2750, SCREEN_HEIGHT - 250, "special"),  # Ajustado de 3300 para 2750
        ]
        
        for x, y, coin_type in coin_positions:
            if coin_type == "special":
                coin = PowerUpCoin(x, y)
            elif coin_type == "bonus":
                coin = BonusCoin(x, y)
            else:
                coin = Coin(x, y)
            self.coins.add(coin)
            self.all_sprites.add(coin)
        
        # Inimigos alinhados com as plataformas (ajustados para novas posições)
        enemy_positions = [
            (400, SCREEN_HEIGHT - 200),   # Alinhado com plataforma wood (350-530)
            (880, SCREEN_HEIGHT - 170),   # Alinhado com plataforma stone (830-980)
            (1570, SCREEN_HEIGHT - 170),  # Alinhado com plataforma stone (1520-1720)
            (2400, SCREEN_HEIGHT - 210),  # Alinhado com plataforma final (2350-2650)
        ]
        
        for x, y in enemy_positions:
            enemy = Enemy(x, y, self.platforms)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

    def create_level_2(self):
        """Cria o segundo nível - Desafio Intermediário Mais Fácil"""
        print("🎮 Criando Nível 2 - Desafio Intermediário")
        
        # Plataformas muito mais acessíveis (espaçamentos mínimos)
        platforms_data = [
            # Início com progressão muito suave
            (0, SCREEN_HEIGHT - 100, 200, 40, "stone"),
            (200, SCREEN_HEIGHT - 160, 150, 40, "wood"),      # Reduzido de 220 para 200, aumentado largura
            (350, SCREEN_HEIGHT - 220, 130, 40, "normal"),    # Reduzido de 380 para 350, aumentado largura
            (480, SCREEN_HEIGHT - 280, 120, 40, "normal"),    # Reduzido de 520 para 480, removido gelo escorregadio
            
            # Seção de plataformas especiais (sem obstáculos difíceis)
            (600, SCREEN_HEIGHT - 200, 120, 40, "wood"),      # Reduzido de 640 para 600, aumentado largura
            (720, SCREEN_HEIGHT - 280, 130, 40, "normal"),    # Reduzido de 760 para 720, mudado de cloud para normal
            (850, SCREEN_HEIGHT - 180, 120, 40, "wood"),      # Reduzido de 890 para 850, removido disappear
            (970, SCREEN_HEIGHT - 240, 140, 40, "normal"),    # Reduzido de 1010 para 970, removido bounce
            
            # Seção de desafio muito acessível
            (1110, SCREEN_HEIGHT - 320, 120, 40, "stone"),    # Reduzido de 1150 para 1110, aumentado largura
            (1230, SCREEN_HEIGHT - 260, 130, 40, "wood"),     # Reduzido de 1270 para 1230, aumentado largura
            (1360, SCREEN_HEIGHT - 200, 140, 40, "normal"),   # Reduzido de 1400 para 1360, aumentado largura
            (1500, SCREEN_HEIGHT - 280, 120, 40, "normal"),   # Reduzido de 1540 para 1500, removido gelo
            
            # Seção de precisão muito fácil
            (1620, SCREEN_HEIGHT - 360, 110, 40, "normal"),   # Reduzido de 1660 para 1620, mudado de cloud para normal
            (1730, SCREEN_HEIGHT - 300, 120, 40, "normal"),   # Reduzido de 1770 para 1730, aumentado largura
            (1850, SCREEN_HEIGHT - 240, 130, 40, "wood"),     # Reduzido de 1890 para 1850, aumentado largura
            (1980, SCREEN_HEIGHT - 180, 140, 40, "stone"),    # Reduzido de 2020 para 1980, aumentado largura
            
            # Seção final muito acessível
            (2120, SCREEN_HEIGHT - 260, 120, 40, "normal"),   # Reduzido de 2160 para 2120, aumentado largura
            (2240, SCREEN_HEIGHT - 200, 130, 40, "wood"),     # Reduzido de 2280 para 2240, removido bounce
            (2370, SCREEN_HEIGHT - 280, 160, 40, "grass"),    # Reduzido de 2410 para 2370, aumentado largura
            (2530, SCREEN_HEIGHT - 200, 220, 40, "stone"),    # Reduzido de 2570 para 2530, aumentado largura
        ]
        
        # Cria plataformas simples (sem obstáculos especiais)
        for x, y, width, height, platform_type in platforms_data:
            platform = Platform(x, y, width, height, platform_type)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
        
        # Moedas melhor distribuídas (mais fáceis de coletar)
        coin_positions = [
            (250, SCREEN_HEIGHT - 210, "normal"),      # Ajustado para nova posição
            (400, SCREEN_HEIGHT - 270, "bonus"),       # Ajustado para nova posição
            (530, SCREEN_HEIGHT - 330, "special"),     # Ajustado para nova posição
            (650, SCREEN_HEIGHT - 250, "normal"),      # Ajustado para nova posição
            (770, SCREEN_HEIGHT - 330, "bonus"),       # Ajustado para nova posição
            (900, SCREEN_HEIGHT - 230, "normal"),      # Ajustado para nova posição
            (1020, SCREEN_HEIGHT - 290, "special"),    # Ajustado para nova posição
            (1160, SCREEN_HEIGHT - 370, "bonus"),      # Ajustado para nova posição
            (1280, SCREEN_HEIGHT - 310, "normal"),     # Ajustado para nova posição
            (1410, SCREEN_HEIGHT - 250, "special"),    # Ajustado para nova posição
            (1550, SCREEN_HEIGHT - 330, "bonus"),      # Ajustado para nova posição
            (1670, SCREEN_HEIGHT - 410, "special"),    # Ajustado para nova posição
            (1780, SCREEN_HEIGHT - 350, "normal"),     # Ajustado para nova posição
            (1900, SCREEN_HEIGHT - 290, "bonus"),      # Ajustado para nova posição
            (2030, SCREEN_HEIGHT - 230, "normal"),     # Ajustado para nova posição
            (2170, SCREEN_HEIGHT - 310, "special"),    # Ajustado para nova posição
            (2290, SCREEN_HEIGHT - 250, "bonus"),      # Ajustado para nova posição
            (2420, SCREEN_HEIGHT - 330, "special"),    # Ajustado para nova posição
            (2580, SCREEN_HEIGHT - 250, "normal"),     # Ajustado para nova posição
        ]
        
        for x, y, coin_type in coin_positions:
            if coin_type == "special":
                coin = PowerUpCoin(x, y)
            elif coin_type == "bonus":
                coin = BonusCoin(x, y)
            else:
                coin = Coin(x, y)
            self.coins.add(coin)
            self.all_sprites.add(coin)
        
        # Inimigos muito mais fáceis (ainda menos inimigos)
        enemy_positions = [
            (650, SCREEN_HEIGHT - 250),   # Plataforma wood
            (1160, SCREEN_HEIGHT - 370),  # Plataforma stone
            (1780, SCREEN_HEIGHT - 350),  # Plataforma normal
            (2420, SCREEN_HEIGHT - 330),  # Plataforma grass
        ]
        
        for x, y in enemy_positions:
            enemy = Enemy(x, y, self.platforms)
            enemy.health = 1  # Inimigos fracos
            enemy.speed = ENEMY_SPEED * 0.7  # Ainda mais lentos
            enemy.detection_range = 80  # Detecção ainda menor
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

    def handle_events(self):
        """Gerencia eventos do jogo"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.game_state == GAME_MENU:
                    self.handle_menu_input(event.key)
                elif self.game_state == GAME_PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = GAME_PAUSED
                elif self.game_state == GAME_PAUSED:
                    self.handle_pause_input(event.key)
                elif self.game_state == GAME_OVER:
                    if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        self.reset_game()
                        self.game_state = GAME_MENU
                elif self.game_state == GAME_COMPLETE:
                    if event.key == pygame.K_r:  # Reiniciar jogo
                        print("🔄 Reiniciando jogo...")
                        self.reset_game()
                        self.start_game()
                    elif event.key in [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]:  # Voltar ao menu
                        print("🏠 Voltando ao menu...")
                        self.reset_game()
                        self.game_state = GAME_MENU
    
    def handle_menu_input(self, key):
        """Gerencia input do menu"""
        if key in [pygame.K_UP, pygame.K_w]:
            self.menu_selection = (self.menu_selection - 1) % len(self.menu_options)
        elif key in [pygame.K_DOWN, pygame.K_s]:
            self.menu_selection = (self.menu_selection + 1) % len(self.menu_options)
        elif key in [pygame.K_RETURN, pygame.K_SPACE]:
            if self.menu_selection == 0:  # JOGAR
                self.start_game()
            elif self.menu_selection == 1:  # SAIR
                self.running = False
    
    def handle_pause_input(self, key):
        """Gerencia input do pause"""
        if key in [pygame.K_UP, pygame.K_w]:
            self.pause_selection = (self.pause_selection - 1) % len(self.pause_options)
        elif key in [pygame.K_DOWN, pygame.K_s]:
            self.pause_selection = (self.pause_selection + 1) % len(self.pause_options)
        elif key in [pygame.K_RETURN, pygame.K_SPACE]:
            if self.pause_selection == 0:  # CONTINUAR
                self.game_state = GAME_PLAYING
            elif self.pause_selection == 1:  # MENU
                self.game_state = GAME_MENU
            elif self.pause_selection == 2:  # SAIR
                self.running = False
        elif key == pygame.K_ESCAPE:
            self.game_state = GAME_PLAYING
    
    def start_game(self):
        """Inicia o jogo"""
        self.reset_game()
        self.create_level(self.level)
        self.game_state = GAME_PLAYING
    
    def reset_game(self):
        """Reseta o jogo"""
        self.score = 0
        self.level = 1
        self.lives = INITIAL_LIVES
        self.time_remaining = 300
        self.game_timer = 0
        self.coins_collected = 0
        self.enemies_defeated = 0
        self.screen_shake = 0
        self.fade_alpha = 0
        self.transition_timer = 0

    def update(self):
        """Atualização principal do jogo"""
        if self.game_state == GAME_PLAYING:
            self.update_game()
        
        # Atualiza efeitos visuais
        if self.screen_shake > 0:
            self.screen_shake -= 1
        
        if self.transition_timer > 0:
            self.transition_timer -= 1
    
    def update_game(self):
        """Atualiza lógica do jogo"""
        # Atualiza timer
        self.game_timer += 1
        if self.game_timer % 60 == 0:  # A cada segundo
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.game_over()
                return
        
        # Atualiza sprites individualmente para controlar parâmetros
        # Atualiza plataformas
        self.platforms.update()
        
        # Atualiza moedas
        self.coins.update()
        
        # Atualiza o player
        if self.player:
            self.player.update()
        
        # Atualiza inimigos passando o player como parâmetro
        for enemy in self.enemies:
            enemy.update(self.player)
        
        # Atualiza câmera
        if self.player:
            self.camera.update(self.player)
        
        # Verifica colisões
        self.check_collisions()

        # Verifica condições de vitória/derrota
        self.check_game_conditions()

    def check_collisions(self):
        """Verifica todas as colisões"""
        if not self.player:
            return
        
        # Colisão jogador-moedas
        collected_coins = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in collected_coins:
            self.score += coin.value
            self.coins_collected += 1
            
            if self.coin_sound:
                self.coin_sound.play()

        # Colisão jogador-inimigos
        if not self.player.invulnerable:
            hit_enemies = pygame.sprite.spritecollide(self.player, self.enemies, False)
            for enemy in hit_enemies:
                if self.player.take_damage():
                    self.game_over()
                    return
                else:
                    self.lives -= 1
                    self.screen_shake = 20
        
        # Ataque do jogador
        if self.player.is_attacking:
            attack_rect = self.player.get_attack_rect()
            if attack_rect:
                hit_enemies = [enemy for enemy in self.enemies if attack_rect.colliderect(enemy.rect)]
                for enemy in hit_enemies:
                    if enemy.take_damage(self.player.attack_damage):
                        self.enemies.remove(enemy)
                        self.all_sprites.remove(enemy)
                        self.enemies_defeated += 1
                        self.score += 50
        
        # Verifica se o jogador caiu do mapa
        if self.player.rect.y > SCREEN_HEIGHT + 100:
            if self.player.take_damage(1):
                self.game_over()
            else:
                self.lives -= 1
                # Reposiciona o jogador
                self.player.reset_position(100, SCREEN_HEIGHT - 200)
                self.screen_shake = 15
    
    def check_game_conditions(self):
        """Verifica condições de vitória/derrota"""
        if not self.player:
            return
        
        # Verifica se chegou ao final do nível baseado no nível atual
        if self.level == 1:
            # Nível 1: última plataforma termina em X=2900 (2700 + 200)
            end_position = 2900
        elif self.level == 2:
            # Nível 2: última plataforma termina em X=2750 (2530 + 220)
            end_position = 2750
        else:
            # Fallback para outros níveis
            end_position = WORLD_WIDTH - 200
        
        if self.player.rect.x >= end_position:
            print(f"🏁 Jogador chegou ao final do nível {self.level}! Posição: {self.player.rect.x}")
            self.next_level()
        
        # Verifica se coletou todas as moedas (bônus alternativo)
        if len(self.coins) == 0:
            print(f"🪙 Todas as moedas coletadas no nível {self.level}!")
            self.score += 1000  # Bônus por coletar tudo
            self.next_level()
    
    def next_level(self):
        """Avança para o próximo nível"""
        print(f"🎯 Avançando do nível {self.level} (max: {self.max_level})")
        
        if self.level < self.max_level:
            self.level += 1
            self.score += self.time_remaining * 10  # Bônus de tempo
            self.time_remaining = 300  # Reset do tempo
            print(f"🆙 Avançando para nível {self.level}")
            self.create_level(self.level)
            self.transition_timer = 60
            self.fade_alpha = 255
        else:
            print("🎉 Jogo completo! Todas as fases foram concluídas!")
            self.game_complete()
    
    def game_over(self):
        """Game Over"""
        self.game_state = GAME_OVER
        if self.score > self.best_score:
            self.best_score = self.score
        
        if self.game_over_sound:
            self.game_over_sound.play()
    
    def game_complete(self):
        """Jogo completo"""
        print("🏆 JOGO COMPLETO! Mudando para tela de conclusão...")
        self.game_state = GAME_COMPLETE
        self.score += 5000  # Bônus de conclusão
        if self.score > self.best_score:
            self.best_score = self.score
        print(f"📊 Pontuação final: {self.score} (melhor: {self.best_score})")
    
    def draw(self):
        """Desenha tudo na tela"""
        # Efeito de screen shake
        shake_offset = (0, 0)
        if self.screen_shake > 0:
            shake_offset = (random.randint(-3, 3), random.randint(-3, 3))
        
        if self.game_state == GAME_MENU:
            self.draw_menu()
        elif self.game_state == GAME_PLAYING:
            self.draw_game(shake_offset)
        elif self.game_state == GAME_PAUSED:
            self.draw_game(shake_offset)
            self.draw_pause_overlay()
        elif self.game_state == GAME_OVER:
            self.draw_game_over()
        elif self.game_state == GAME_COMPLETE:
            self.draw_game_complete()
        
        # Efeito de transição
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.fill(BLACK)
            fade_surface.set_alpha(self.fade_alpha)
            self.screen.blit(fade_surface, (0, 0))
            self.fade_alpha = max(0, self.fade_alpha - 5)
        
        pygame.display.flip()
    
    def draw_menu(self):
        """Desenha o menu principal - versão simplificada"""
        # Fundo simples
        self.screen.fill((20, 20, 40))
        
        # Título
        title = "SUPER HERO"
        draw_text(self.screen, title, 72, SCREEN_WIDTH // 2, 150, GOLD, self.font_large)
        
        # Subtítulo
        subtitle = "Jogo de Plataforma"
        draw_text(self.screen, subtitle, 36, SCREEN_WIDTH // 2, 220, WHITE, self.font_medium)
        
        # Opções do menu
        menu_y = 350
        spacing = 80
        
        menu_options = [
            "Pressione ENTER para Jogar",
            "Pressione ESC para Sair"
        ]
        
        for i, option in enumerate(menu_options):
            color = YELLOW if i == 0 else LIGHT_GRAY
            draw_text(self.screen, option, 32, SCREEN_WIDTH // 2, menu_y + i * spacing, color, self.font_medium)
        
        # Instruções
        instructions = [
            "Controles:",
            "WASD ou Setas - Mover",
            "ESPAÇO - Pular",
            "X - Atacar"
        ]
        
        inst_y = 550
        for i, instruction in enumerate(instructions):
            color = WHITE if i == 0 else LIGHT_GRAY
            size = 24 if i == 0 else 20
            draw_text(self.screen, instruction, size, SCREEN_WIDTH // 2, inst_y + i * 25, color, self.font_small)
    
    def draw_game(self, shake_offset=(0, 0)):
        """Desenha o jogo"""
        # Fundo simples
        self.screen.fill(SKY_BLUE)
        
        # Se tiver imagem de fundo, desenha como pattern
        if self.background:
            bg_x = -(self.camera.camera.x * 0.3) % self.background.get_width()
            self.screen.blit(self.background, (bg_x - self.background.get_width(), 0))
            self.screen.blit(self.background, (bg_x, 0))
            if bg_x + self.background.get_width() < SCREEN_WIDTH:
                self.screen.blit(self.background, (bg_x + self.background.get_width(), 0))
        
        # Sprites
        for sprite in self.all_sprites:
            offset_rect = self.camera.apply(sprite)
            offset_rect.x += shake_offset[0]
            offset_rect.y += shake_offset[1]
            self.screen.blit(sprite.image, offset_rect)
        
        # HUD
        self.draw_hud()
    
    def draw_hud(self):
        """Desenha a interface do usuário - versão simplificada"""
        # Painel do HUD com fundo mais simples
        hud_rect = pygame.Rect(0, 0, SCREEN_WIDTH, HUD_HEIGHT)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), hud_rect)
        pygame.draw.rect(self.screen, WHITE, hud_rect, 2)
        
        margin = 20
        y_pos = 25
        
        # Vidas
        lives_text = f"Vidas: {self.lives}"
        draw_text_left(self.screen, lives_text, 28, margin, y_pos, RED, self.font_medium)
        
        # Pontuação (centro)
        score_text = f"Pontuação: {self.score:,}"
        draw_text(self.screen, score_text, 28, SCREEN_WIDTH // 2, y_pos, GOLD, self.font_medium)
        
        # Nível (direita)
        level_text = f"Nível: {self.level}/{self.max_level}"
        draw_text_right(self.screen, level_text, 28, SCREEN_WIDTH - margin, y_pos, WHITE, self.font_medium)
        
        # Segunda linha
        y_pos2 = 55
        
        # Tempo
        time_minutes = self.time_remaining // 60
        time_seconds = self.time_remaining % 60
        time_text = f"Tempo: {time_minutes:02d}:{time_seconds:02d}"
        time_color = RED if self.time_remaining < 60 else WHITE
        draw_text_left(self.screen, time_text, 22, margin, y_pos2, time_color, self.font_small)
        
        # Estatísticas
        stats_text = f"Moedas: {self.coins_collected} | Inimigos: {self.enemies_defeated}"
        draw_text_right(self.screen, stats_text, 22, SCREEN_WIDTH - margin, y_pos2, LIGHT_GRAY, self.font_small)
        
        # Barra de vida do jogador (mais simples)
        if self.player:
            health_x = SCREEN_WIDTH // 2 - 75
            health_y = y_pos2 + 5
            health_width = 150
            health_height = 12
            
            # Fundo da barra
            pygame.draw.rect(self.screen, (100, 0, 0), (health_x, health_y, health_width, health_height))
            
            # Vida atual
            current_health_width = int(health_width * (self.player.health / self.player.max_health))
            if current_health_width > 0:
                pygame.draw.rect(self.screen, (0, 200, 0), (health_x, health_y, current_health_width, health_height))
            
            # Borda
            pygame.draw.rect(self.screen, WHITE, (health_x, health_y, health_width, health_height), 1)
    
    def draw_pause_overlay(self):
        """Desenha overlay de pausa - versão simplificada"""
        # Overlay semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Texto de pausa
        draw_text(self.screen, "JOGO PAUSADO", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, WHITE, self.font_large)
        draw_text(self.screen, "Pressione ESC para continuar", 32, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, LIGHT_GRAY, self.font_medium)
    
    def draw_game_over(self):
        """Desenha tela de game over - versão simplificada"""
        # Fundo escuro
        self.screen.fill((40, 0, 0))
        
        # Título
        draw_text(self.screen, "GAME OVER", 72, SCREEN_WIDTH // 2, 200, RED, self.font_large)
        
        # Estatísticas
        stats_y = 320
        spacing = 40
        
        stats = [
            f"Pontuação Final: {self.score:,}",
            f"Nível Alcançado: {self.level}",
            f"Moedas Coletadas: {self.coins_collected}",
            f"Inimigos Derrotados: {self.enemies_defeated}"
        ]
        
        for i, stat in enumerate(stats):
            draw_text(self.screen, stat, 28, SCREEN_WIDTH // 2, stats_y + i * spacing, WHITE, self.font_medium)
        
        # Instruções
        draw_text(self.screen, "Pressione R para reiniciar ou ESC para sair", 24, SCREEN_WIDTH // 2, 550, YELLOW, self.font_small)
    
    def draw_game_complete(self):
        """Desenha tela de jogo completo - Parabéns personalizada"""
        # Fundo com gradiente dourado
        self.screen.fill((25, 20, 5))
        
        # Efeito de brilho no fundo
        for i in range(5):
            alpha = 20 - i * 3
            color = (60 + i * 10, 50 + i * 8, 10 + i * 2)
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(alpha)
            overlay.fill(color)
            self.screen.blit(overlay, (0, 0))
        
        # Título principal com efeito
        title_y = 120
        draw_text(self.screen, "🎉 PARABÉNS! 🎉", 80, SCREEN_WIDTH // 2, title_y, GOLD, self.font_large)
        
        # Subtítulo
        subtitle_y = 200
        draw_text(self.screen, "Você completou Super Hero!", 42, SCREEN_WIDTH // 2, subtitle_y, WHITE, self.font_medium)
        
        # Mensagem de conquista
        achievement_y = 260
        draw_text(self.screen, "Todas as fases foram superadas com sucesso!", 28, SCREEN_WIDTH // 2, achievement_y, YELLOW, self.font_medium)
        
        # Caixa de estatísticas com fundo
        stats_box = pygame.Rect(SCREEN_WIDTH // 2 - 200, 320, 400, 180)
        pygame.draw.rect(self.screen, (40, 30, 10), stats_box)
        pygame.draw.rect(self.screen, GOLD, stats_box, 3)
        
        # Título das estatísticas
        draw_text(self.screen, "📊 ESTATÍSTICAS FINAIS", 32, SCREEN_WIDTH // 2, 340, GOLD, self.font_medium)
        
        # Estatísticas detalhadas
        stats_y = 380
        spacing = 30
        
        stats = [
            f"🏆 Pontuação Total: {self.score:,}",
            f"🪙 Moedas Coletadas: {self.coins_collected}",
            f"⚔️ Inimigos Derrotados: {self.enemies_defeated}",
            f"⏱️ Tempo Restante: {self.time_remaining // 60}:{self.time_remaining % 60:02d}"
        ]
        
        for i, stat in enumerate(stats):
            draw_text(self.screen, stat, 24, SCREEN_WIDTH // 2, stats_y + i * spacing, WHITE, self.font_small)
        
        # Mensagem de agradecimento
        thanks_y = 530
        draw_text(self.screen, "Obrigado por jogar Super Hero!", 28, SCREEN_WIDTH // 2, thanks_y, LIGHT_GRAY, self.font_medium)
        
        # Instruções para reiniciar com destaque
        restart_box = pygame.Rect(SCREEN_WIDTH // 2 - 280, 580, 560, 100)
        pygame.draw.rect(self.screen, (20, 40, 20), restart_box)
        pygame.draw.rect(self.screen, GREEN, restart_box, 2)
        
        draw_text(self.screen, "🔄 Pressione R para jogar novamente", 26, SCREEN_WIDTH // 2, 600, GREEN, self.font_medium)
        draw_text(self.screen, "🏠 Pressione ESC, ENTER ou ESPAÇO para voltar ao menu", 20, SCREEN_WIDTH // 2, 630, LIGHT_GRAY, self.font_small)
        draw_text(self.screen, "🚪 Pressione Alt+F4 para sair do jogo", 18, SCREEN_WIDTH // 2, 655, GRAY, self.font_small)
        
        # Efeito de partículas douradas (simulado com pontos)
        for _ in range(20):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(1, 3)
            alpha = random.randint(100, 255)
            color = (255, 215, 0, alpha)  # Dourado
            pygame.draw.circle(self.screen, color[:3], (x, y), size)
    
    def run(self):
        """Loop principal do jogo"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
