import pygame
import math
import os
from game.settings import *
from game.utils import load_image, load_sprite

class Player(pygame.sprite.Sprite):
    """Classe do jogador principal com animação estável"""
    
    def __init__(self, x, y, platform_group):
        super().__init__()
        
        # Posição inicial
        self.start_x = x
        self.start_y = y
        
        # Carregamento de sprites
        self.sprites = {}
        self.load_sprites()
        
        # Rect e posição
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Referência às plataformas
        self.platform_group = platform_group
        
        # ===== FÍSICA SIMPLIFICADA =====
        
        # Velocidade
        self.velocity = pygame.math.Vector2(0, 0)
        
        # Estados de física
        self.on_ground = False
        self.can_jump = True
        self.ground_platform = None
        
        # Movimento
        self.speed = PLAYER_SPEED
        self.jump_strength = JUMP_STRENGTH
        self.facing_right = True
        
        # ===== ANIMAÇÃO ESTÁVEL =====
        
        # Estado atual FIXO - só muda quando realmente necessário
        self.current_state = 'IDLE'
        self.last_state = 'IDLE'
        self.state_changed = False
        
        # Controle de animação
        self.animation_locked = False
        self.animation_lock_timer = 0
        
        # Estados de movimento
        self.is_moving = False
        self.is_jumping = False
        self.is_falling = False
        self.is_attacking = False
        
        # Vida e combate
        self.health = 3
        self.max_health = 3
        self.attack_damage = 1
        self.attack_timer = 0
        self.attack_cooldown = 30
        
        # Invulnerabilidade
        self.invulnerable = False
        self.invulnerability_timer = 0
        self.blink_timer = 0
        
        # Sons
        self.jump_sound = None
        self.attack_sound = None
        try:
            from game.utils import load_sound
            self.jump_sound = load_sound(JUMP_SOUND, 0.4)
            self.attack_sound = load_sound(ATTACK_SOUND, 0.3)
        except:
            pass
    
    def load_sprites(self):
        """Carrega sprites do jogador"""
        sprite_files = {
            'IDLE': 'pparado.png',
            'WALK': 'pandando.png',
            'JUMP': 'ppulando.png',
            'ATTACK': 'patacando.png'
        }
        
        for state, filename in sprite_files.items():
            path = os.path.join('assets', 'images', filename)
            sprite = load_sprite(path, (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.sprites[state] = sprite
        
        # Sprite inicial
        self.image = self.sprites['IDLE']
        self.current_state = 'IDLE'
    
    def update(self):
        """Atualização principal simplificada"""
        # Atualiza física
        self.update_physics()
        
        # Atualiza entrada
        self.handle_input()
        
        # Determina estado atual
        self.determine_state()
        
        # Aplica sprite apenas se mudou
        self.apply_sprite()
        
        # Atualiza timers
        self.update_timers()
        
        # Verifica limites
        self.check_boundaries()
    
    def update_physics(self):
        """Física simplificada e estável"""
        # Gravidade
        if not self.on_ground:
            self.velocity.y += GRAVITY
            if self.velocity.y > MAX_FALL_SPEED:
                self.velocity.y = MAX_FALL_SPEED
        
        # Aplica movimento horizontal
        self.rect.x += int(self.velocity.x)
        self.check_platform_collision_x()
        
        # Aplica movimento vertical
        self.rect.y += int(self.velocity.y)
        self.check_platform_collision_y()
        
        # Atrito no chão
        if self.on_ground:
            self.velocity.x *= 0.8
            if abs(self.velocity.x) < 0.1:
                self.velocity.x = 0
    
    def handle_input(self):
        """Controle de entrada simplificado"""
        keys = pygame.key.get_pressed()
        
        # Reset do movimento
        self.is_moving = False
        
        # Movimento horizontal
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -self.speed
            self.facing_right = False
            self.is_moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = self.speed
            self.facing_right = True
            self.is_moving = True
        
        # Salto
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.can_jump:
            self.jump()
        
        # Ataque
        if keys[pygame.K_x] and self.attack_timer <= 0:
            self.attack()
    
    def jump(self):
        """Pulo simplificado"""
        if self.on_ground:
            self.velocity.y = self.jump_strength
            self.on_ground = False
            self.can_jump = False
            self.is_jumping = True
            
            if self.jump_sound:
                self.jump_sound.play()
    
    def attack(self):
        """Ataque simplificado"""
        self.is_attacking = True
        self.attack_timer = self.attack_cooldown
        self.animation_locked = True
        self.animation_lock_timer = 15  # Trava animação por 15 frames
        
        if self.attack_sound:
            self.attack_sound.play()
    
    def determine_state(self):
        """Determina o estado atual do jogador de forma estável"""
        # Salva estado anterior
        self.last_state = self.current_state
        
        # Determina novo estado baseado em prioridades
        if self.is_attacking and self.attack_timer > self.attack_cooldown - 15:
            new_state = 'ATTACK'
        elif self.velocity.y < -2:  # Pulando
            new_state = 'JUMP'
        elif self.velocity.y > 2:   # Caindo
            new_state = 'JUMP'  # Usa mesma animação
        elif self.is_moving and abs(self.velocity.x) > 1:
            new_state = 'WALK'
        else:
            new_state = 'IDLE'
        
        # Só muda se for diferente E não estiver travado (exceto para ataque)
        if new_state != self.current_state and (not self.animation_locked or new_state == 'ATTACK'):
            self.current_state = new_state
            self.state_changed = True
        else:
            self.state_changed = False
    
    def apply_sprite(self):
        """Aplica sprite apenas quando necessário"""
        # Só atualiza sprite se mudou de estado
        if self.state_changed or self.current_state not in self.sprites:
            
            # Usa sprite do estado atual
            if self.current_state in self.sprites:
                base_sprite = self.sprites[self.current_state]
            else:
                base_sprite = self.sprites['IDLE']
            
            # Cria nova imagem
            self.image = base_sprite.copy()
            
            # Espelha se necessário
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
            
            # Aplica efeito de invulnerabilidade (sem piscar excessivo)
            if self.invulnerable and self.blink_timer % 20 < 10:
                # Efeito mais sutil
                overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 100))
                self.image.blit(overlay, (0, 0))
    
    def check_platform_collision_x(self):
        """Colisão horizontal simplificada"""
        collisions = pygame.sprite.spritecollide(self, self.platform_group, False)
        for platform in collisions:
            if self.velocity.x > 0:
                self.rect.right = platform.rect.left
                self.velocity.x = 0
            elif self.velocity.x < 0:
                self.rect.left = platform.rect.right
                self.velocity.x = 0
    
    def check_platform_collision_y(self):
        """Colisão vertical simplificada"""
        self.on_ground = False
        self.ground_platform = None
        
        collisions = pygame.sprite.spritecollide(self, self.platform_group, False)
        
        for platform in collisions:
            if self.velocity.y > 0:  # Caindo
                if self.rect.bottom <= platform.rect.top + 10:
                    self.rect.bottom = platform.rect.top
                    self.velocity.y = 0
                    self.on_ground = True
                    self.can_jump = True
                    self.is_jumping = False
                    self.ground_platform = platform
                    break
            elif self.velocity.y < 0:  # Subindo
                if self.rect.top >= platform.rect.bottom - 10:
                    self.rect.top = platform.rect.bottom
                    self.velocity.y = 0
                    break
    
    def get_attack_rect(self):
        """Retorna retângulo de ataque"""
        if not self.is_attacking or self.attack_timer <= self.attack_cooldown - 15:
            return None
        
        attack_width = 40
        attack_height = 30
        
        if self.facing_right:
            attack_x = self.rect.right
        else:
            attack_x = self.rect.left - attack_width
        
        attack_y = self.rect.centery - attack_height // 2
        
        return pygame.Rect(attack_x, attack_y, attack_width, attack_height)
    
    def take_damage(self, damage=1):
        """Recebe dano"""
        if self.invulnerable:
            return False
        
        self.health -= damage
        self.invulnerable = True
        self.invulnerability_timer = INVULNERABILITY_TIME
        
        # Knockback simples
        if self.facing_right:
            self.velocity.x = -8
        else:
            self.velocity.x = 8
        
        return self.health <= 0
    
    def heal(self, amount=1):
        """Cura o jogador"""
        self.health = min(self.health + amount, self.max_health)
    
    def reset_position(self, x, y):
        """Reposiciona o jogador"""
        self.rect.x = x
        self.rect.y = y
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.health = self.max_health
        self.invulnerable = False
        self.invulnerability_timer = 0
        self.current_state = 'IDLE'
    
    def update_timers(self):
        """Atualiza timers"""
        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False
        
        if self.animation_lock_timer > 0:
            self.animation_lock_timer -= 1
            if self.animation_lock_timer <= 0:
                self.animation_locked = False
        
        if self.invulnerability_timer > 0:
            self.invulnerability_timer -= 1
            self.blink_timer += 1
            if self.invulnerability_timer <= 0:
                self.invulnerable = False
                self.blink_timer = 0
    
    def check_boundaries(self):
        """Verifica limites do mundo"""
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity.x = 0
        elif self.rect.right > WORLD_WIDTH:
            self.rect.right = WORLD_WIDTH
            self.velocity.x = 0
        
        # Se caiu do mundo, reposiciona
        if self.rect.y > WORLD_HEIGHT + 100:
            self.reset_position(self.start_x, self.start_y)
            self.health -= 1
