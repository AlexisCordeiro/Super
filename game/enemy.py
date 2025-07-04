import pygame
import random
import math
import os
from game.settings import *
from game.utils import load_image, clamp, load_sprite

class Enemy(pygame.sprite.Sprite):
    """Classe dos inimigos com movimento fixo nas plataformas"""
    
    def __init__(self, x, y, platform_group):
        super().__init__()
        
        # Carregamento de sprites primeiro
        self.load_sprites()
        
        # Rect e posição
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.start_x = x
        self.start_y = y
        
        # Referência às plataformas
        self.platform_group = platform_group
        
        # ===== FÍSICA SIMPLIFICADA =====
        
        # Velocidade
        self.velocity = pygame.math.Vector2(0, 0)
        
        # Estados de física
        self.on_ground = False
        self.ground_platform = None
        self.platform_bounds = None  # Limites da plataforma atual
        
        # ===== MOVIMENTO CONTROLADO =====
        
        # Direção e patrulhamento
        self.direction = random.choice([-1, 1])
        self.speed = ENEMY_SPEED
        self.facing_right = self.direction > 0
        
        # Limites de movimento (baseados na plataforma)
        self.patrol_left = x - 60
        self.patrol_right = x + 60
        self.patrol_center = x
        
        # Controle de movimento
        self.move_timer = 0
        self.pause_timer = 0
        self.stuck_timer = 0
        self.last_x = x
        
        # Estados
        self.state = 'PATROL'  # PATROL, ALERT, ATTACK, DAMAGED
        self.current_sprite_state = 'IDLE'
        
        # Vida e combate
        self.health = 2
        self.max_health = 2
        self.damage = 1
        self.attack_range = 60
        self.detection_range = 120
        
        # Timers
        self.damage_timer = 0
        self.state_timer = 0
        self.animation_timer = 0
        
        # Encontra plataforma inicial
        self.find_initial_platform()
    
    def load_sprites(self):
        """Carrega sprites do inimigo de forma simplificada"""
        try:
            # Carrega sprites usando load_image
            self.sprites = {}
            
            # Caminhos dos sprites (caminho completo)
            sprite_files = {
                'IDLE': os.path.join('assets', 'images', 'vparado.png'),
                'WALKING': os.path.join('assets', 'images', 'vandando.png'),
                'ATTACKING': os.path.join('assets', 'images', 'vatacando.png'),
                'DAMAGE': os.path.join('assets', 'images', 'vsofrendo.png')
            }
            
            # Carrega cada sprite
            for state, filepath in sprite_files.items():
                try:
                    sprite = load_image(filepath, (ENEMY_WIDTH, ENEMY_HEIGHT))
                    self.sprites[state] = sprite
                    print(f"✅ Sprite {state} carregado com sucesso!")
                except Exception as e:
                    print(f"❌ Erro ao carregar sprite {filepath}: {e}")
                    # Cria um sprite de fallback
                    fallback_sprite = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
                    fallback_sprite.fill((150, 0, 0))  # Vermelho escuro
                    self.sprites[state] = fallback_sprite
            
            # Define sprite inicial
            self.image = self.sprites['IDLE']
            self.current_sprite_state = 'IDLE'
            
        except Exception as e:
            print(f"❌ Erro geral ao carregar sprites do inimigo: {e}")
            # Cria sprite de emergência
            self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
            self.image.fill((200, 0, 0))  # Vermelho
            self.sprites = {'IDLE': self.image}
            self.current_sprite_state = 'IDLE'
    
    def find_initial_platform(self):
        """Encontra a plataforma inicial e define limites"""
        # Posiciona o inimigo na plataforma mais próxima
        closest_platform = None
        min_distance = float('inf')
        
        for platform in self.platform_group:
            # Verifica se está sobre a plataforma
            if (self.rect.centerx >= platform.rect.left and 
                self.rect.centerx <= platform.rect.right):
                
                distance = abs(self.rect.bottom - platform.rect.top)
                if distance < min_distance:
                    min_distance = distance
                    closest_platform = platform
        
        if closest_platform:
            # Posiciona na plataforma
            self.rect.bottom = closest_platform.rect.top
            self.ground_platform = closest_platform
            self.on_ground = True
            
            # Define limites de patrulhamento baseados na plataforma
            self.patrol_left = closest_platform.rect.left + 20
            self.patrol_right = closest_platform.rect.right - 20
            self.patrol_center = closest_platform.rect.centerx
            
            # Ajusta posição se necessário
            if self.rect.left < self.patrol_left:
                self.rect.left = self.patrol_left
            elif self.rect.right > self.patrol_right:
                self.rect.right = self.patrol_right
    
    def update(self, player):
        """Atualização principal do inimigo"""
        self.update_ai(player)
        self.update_physics()
        self.apply_sprite()
        self.update_timers()
        self.check_if_stuck()
    
    def update_ai(self, player):
        """IA simplificada com movimento controlado"""
        distance_to_player = self.distance_to(player.rect.center)
        
        # Máquina de estados
        if self.state == 'PATROL':
            if self.pause_timer > 0:
                self.pause_timer -= 1
                self.velocity.x = 0
            else:
                self.patrol_movement()
            
            # Detecta jogador
            if distance_to_player < self.detection_range:
                self.state = 'ALERT'
                self.state_timer = 60
        
        elif self.state == 'ALERT':
            self.velocity.x = 0
            if distance_to_player < self.attack_range:
                self.state = 'ATTACK'
                self.state_timer = 30
            elif self.state_timer <= 0:
                self.state = 'PATROL'
        
        elif self.state == 'ATTACK':
            if distance_to_player > self.attack_range * 1.5:
                self.state = 'ALERT'
                self.state_timer = 30
            elif self.state_timer <= 0:
                self.state = 'PATROL'
        
        elif self.state == 'DAMAGED':
            self.velocity.x *= 0.5
            if self.damage_timer <= 0:
                self.state = 'PATROL'
    
    def patrol_movement(self):
        """Movimento de patrulhamento controlado"""
        if not self.on_ground or not self.ground_platform:
            self.velocity.x = 0
            return
        
        # Verifica limites da plataforma
        if self.direction > 0:  # Movendo para direita
            if self.rect.right >= self.patrol_right:
                self.turn_around()
                return
        else:  # Movendo para esquerda
            if self.rect.left <= self.patrol_left:
                self.turn_around()
                return
        
        # Movimento normal
        self.velocity.x = self.direction * self.speed
        self.facing_right = self.direction > 0
    
    def turn_around(self):
        """Vira o inimigo"""
        self.direction *= -1
        self.facing_right = self.direction > 0
        self.velocity.x = 0
        self.pause_timer = 30  # Pausa por 30 frames
    
    def update_physics(self):
        """Física simplificada - mantém inimigo na plataforma"""
        # Só aplica gravidade se não estiver no chão
        if not self.on_ground:
            self.velocity.y += GRAVITY
            if self.velocity.y > MAX_FALL_SPEED:
                self.velocity.y = MAX_FALL_SPEED
        else:
            self.velocity.y = 0
        
        # Aplica movimento horizontal
        if self.velocity.x != 0:
            self.rect.x += int(self.velocity.x)
            
            # Mantém dentro dos limites da plataforma
            if self.rect.left < self.patrol_left:
                self.rect.left = self.patrol_left
                self.turn_around()
            elif self.rect.right > self.patrol_right:
                self.rect.right = self.patrol_right
                self.turn_around()
        
        # Aplica movimento vertical
        if self.velocity.y != 0:
            self.rect.y += int(self.velocity.y)
            self.check_platform_collision()
        
        # Garante que está na plataforma
        self.ensure_on_platform()
    
    def check_platform_collision(self):
        """Verifica colisão com plataformas"""
        if self.velocity.y > 0:  # Caindo
            for platform in self.platform_group:
                if (self.rect.colliderect(platform.rect) and
                    self.rect.bottom <= platform.rect.top + 10):
                    
                    self.rect.bottom = platform.rect.top
                    self.velocity.y = 0
                    self.on_ground = True
                    self.ground_platform = platform
                    
                    # Atualiza limites de patrulhamento
                    self.patrol_left = platform.rect.left + 20
                    self.patrol_right = platform.rect.right - 20
                    break
    
    def ensure_on_platform(self):
        """Garante que o inimigo está na plataforma"""
        if self.ground_platform:
            # Verifica se ainda está sobre a plataforma
            platform = self.ground_platform
            
            # Se saiu da plataforma horizontalmente, reposiciona
            if (self.rect.right < platform.rect.left or 
                self.rect.left > platform.rect.right):
                
                # Reposiciona para o centro da plataforma
                self.rect.centerx = platform.rect.centerx
                self.velocity.x = 0
                self.turn_around()
            
            # Garante que está no topo da plataforma
            if abs(self.rect.bottom - platform.rect.top) > 5:
                self.rect.bottom = platform.rect.top
                self.velocity.y = 0
                self.on_ground = True
    
    def check_if_stuck(self):
        """Verifica se o inimigo está preso"""
        if abs(self.rect.x - self.last_x) < 1:
            self.stuck_timer += 1
            if self.stuck_timer > 60:  # Preso por 1 segundo
                self.turn_around()
                self.stuck_timer = 0
        else:
            self.stuck_timer = 0
        
        self.last_x = self.rect.x
    
    def apply_sprite(self):
        """Aplica sprite baseado no estado"""
        # Determina sprite baseado no estado
        if self.damage_timer > 0:
            target_state = 'DAMAGE'
        elif self.state == 'ATTACK':
            target_state = 'ATTACKING'
        elif abs(self.velocity.x) > 0.1:
            target_state = 'WALKING'
        else:
            target_state = 'IDLE'
        
        # Aplica sprite (sempre atualiza para garantir espelhamento correto)
        if target_state in self.sprites:
            self.image = self.sprites[target_state].copy()
            self.current_sprite_state = target_state
            
            # Espelha se necessário
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            # Fallback para IDLE se sprite não existir
            self.image = self.sprites['IDLE'].copy()
            self.current_sprite_state = 'IDLE'
            
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
    
    def take_damage(self, damage=1):
        """Recebe dano"""
        self.health -= damage
        self.damage_timer = 30
        self.state = 'DAMAGED'
        
        # Knockback simples
        if self.facing_right:
            self.velocity.x = -3
        else:
            self.velocity.x = 3
        
        return self.health <= 0
    
    def get_attack_rect(self):
        """Retorna retângulo de ataque"""
        if self.state != 'ATTACK':
            return None
        
        attack_width = 35
        attack_height = 25
        
        if self.facing_right:
            attack_x = self.rect.right
        else:
            attack_x = self.rect.left - attack_width
        
        attack_y = self.rect.centery - attack_height // 2
        
        return pygame.Rect(attack_x, attack_y, attack_width, attack_height)
    
    def distance_to(self, point):
        """Calcula distância até um ponto"""
        dx = self.rect.centerx - point[0]
        dy = self.rect.centery - point[1]
        return math.sqrt(dx * dx + dy * dy)
    
    def update_timers(self):
        """Atualiza timers"""
        if self.damage_timer > 0:
            self.damage_timer -= 1
        
        if self.state_timer > 0:
            self.state_timer -= 1
        
        self.animation_timer += 1
    
    def draw_effects(self, screen, camera_x):
        """Desenha efeitos visuais"""
        screen_x = self.rect.x - camera_x
        screen_y = self.rect.y
        
        # Barra de vida se ferido
        if self.health < self.max_health:
            self.draw_health_bar(screen, screen_x, screen_y - 10)
        
        # Indicador de estado
        if self.state == 'ALERT':
            pygame.draw.circle(screen, (255, 255, 100), 
                             (screen_x + self.rect.width // 2, screen_y - 15), 5)
        elif self.damage_timer > 0:
            pygame.draw.circle(screen, (255, 100, 100), 
                             (screen_x + self.rect.width // 2, screen_y - 15), 5)
    
    def draw_health_bar(self, screen, x, y):
        """Desenha barra de vida"""
        bar_width = self.rect.width
        bar_height = 6
        
        # Fundo da barra
        bg_rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(screen, (100, 100, 100), bg_rect)
        
        # Barra de vida
        health_percentage = self.health / self.max_health
        health_width = int(bar_width * health_percentage)
        health_rect = pygame.Rect(x, y, health_width, bar_height)
        
        # Cor baseada na vida
        if health_percentage > 0.6:
            color = (100, 255, 100)
        elif health_percentage > 0.3:
            color = (255, 255, 100)
        else:
            color = (255, 100, 100)
        
        pygame.draw.rect(screen, color, health_rect)
