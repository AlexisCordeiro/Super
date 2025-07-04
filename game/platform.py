import pygame
import math
from game.settings import *
from game.utils import load_image

class Platform(pygame.sprite.Sprite):
    """Classe base para plataformas"""
    
    def __init__(self, x, y, width, height, platform_type='normal'):
        super().__init__()
        
        # Dimensões
        self.width = width
        self.height = height
        self.platform_type = platform_type
        
        # Cria a imagem da plataforma
        self.create_platform_image()
        
        # Posição
        self.rect = pygame.Rect(x, y, width, height)
        self.mask = pygame.mask.from_surface(self.image)
        
        # Propriedades específicas do tipo
        self.setup_platform_properties()
        
        # Efeitos visuais
        self.animation_timer = 0
        self.glow_intensity = 0
        
    def create_platform_image(self):
        """Cria a imagem da plataforma baseada no tipo"""
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        if self.platform_type == 'grass':
            self.create_grass_platform()
        elif self.platform_type == 'stone':
            self.create_stone_platform()
        elif self.platform_type == 'wood':
            self.create_wood_platform()
        elif self.platform_type == 'ice':
            self.create_ice_platform()
        elif self.platform_type == 'cloud':
            self.create_cloud_platform()
        elif self.platform_type == 'lava':
            self.create_lava_platform()
        else:
            self.create_normal_platform()
    
    def create_normal_platform(self):
        """Cria plataforma normal com textura melhorada"""
        # Base marrom
        pygame.draw.rect(self.image, BROWN, (0, 0, self.width, self.height))
        
        # Bordas e detalhes
        pygame.draw.rect(self.image, (101, 50, 0), (0, 0, self.width, self.height), 3)
        
        # Textura com linhas
        for i in range(0, self.width, 20):
            pygame.draw.line(self.image, (120, 60, 0), (i, 5), (i, self.height - 5), 2)
        for i in range(5, self.height, 10):
            pygame.draw.line(self.image, (120, 60, 0), (5, i), (self.width - 5, i), 1)
    
    def create_grass_platform(self):
        """Cria uma plataforma de grama (terra com grama no topo)"""
        # Base de terra
        dirt_color = BROWN
        grass_color = GREEN
        
        # Preenche com cor de terra
        self.image.fill(dirt_color)
        
        # Adiciona grama no topo
        grass_height = 8
        grass_rect = pygame.Rect(0, 0, self.width, grass_height)
        pygame.draw.rect(self.image, grass_color, grass_rect)
        
        # Adiciona textura de grama (pequenas linhas)
        for i in range(0, self.width, 4):
            pygame.draw.line(self.image, (0, 100, 0), (i, 0), (i, grass_height - 2), 1)
        
        # Borda
        pygame.draw.rect(self.image, BLACK, self.image.get_rect(), 1)
    
    def create_stone_platform(self):
        """Cria plataforma de pedra"""
        # Base cinza
        stone_color = (128, 128, 128)
        pygame.draw.rect(self.image, stone_color, (0, 0, self.width, self.height))
        
        # Textura de pedra
        for i in range(0, self.width, 25):
            for j in range(0, self.height, 15):
                # Blocos de pedra individuais
                block_color = (110 + (i + j) % 30, 110 + (i + j) % 30, 110 + (i + j) % 30)
                pygame.draw.rect(self.image, block_color, (i, j, 23, 13))
                pygame.draw.rect(self.image, (90, 90, 90), (i, j, 23, 13), 1)
        
        # Bordas
        pygame.draw.rect(self.image, (80, 80, 80), (0, 0, self.width, self.height), 3)
    
    def create_wood_platform(self):
        """Cria plataforma de madeira"""
        # Base marrom clara
        wood_color = (160, 82, 45)
        pygame.draw.rect(self.image, wood_color, (0, 0, self.width, self.height))
        
        # Tábuas de madeira
        plank_height = self.height // 3
        for i in range(3):
            y_pos = i * plank_height
            # Variação de cor para cada tábua
            plank_color = (150 + i * 10, 75 + i * 5, 40 + i * 3)
            pygame.draw.rect(self.image, plank_color, (0, y_pos, self.width, plank_height))
            
            # Linhas da madeira
            for j in range(0, self.width, 30):
                pygame.draw.line(self.image, (140, 70, 35), (j, y_pos), (j, y_pos + plank_height), 1)
        
        # Bordas
        pygame.draw.rect(self.image, (120, 60, 30), (0, 0, self.width, self.height), 2)
    
    def create_ice_platform(self):
        """Cria plataforma de gelo"""
        # Base azul clara translúcida
        ice_color = (173, 216, 230, 200)
        ice_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        ice_surface.fill(ice_color)
        self.image.blit(ice_surface, (0, 0))
        
        # Efeitos de cristal
        for i in range(0, self.width, 20):
            for j in range(0, self.height, 15):
                crystal_color = (200, 230, 255, 150)
                crystal_surface = pygame.Surface((15, 10), pygame.SRCALPHA)
                crystal_surface.fill(crystal_color)
                self.image.blit(crystal_surface, (i, j))
        
        # Brilho
        highlight_color = (255, 255, 255, 100)
        pygame.draw.rect(self.image, highlight_color, (0, 0, self.width, 3))
        
        # Bordas
        pygame.draw.rect(self.image, (150, 200, 255), (0, 0, self.width, self.height), 2)
    
    def create_cloud_platform(self):
        """Cria plataforma de nuvem"""
        # Base branca fofa
        cloud_color = (255, 255, 255, 180)
        cloud_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Múltiplas camadas para efeito de nuvem
        for i in range(5):
            alpha = 180 - i * 30
            color = (255, 255, 255, max(50, alpha))
            layer_surface = pygame.Surface((self.width - i * 2, self.height - i), pygame.SRCALPHA)
            layer_surface.fill(color)
            cloud_surface.blit(layer_surface, (i, i))
        
        self.image.blit(cloud_surface, (0, 0))
        
        # Contorno suave
        pygame.draw.rect(self.image, (220, 220, 220, 100), (0, 0, self.width, self.height), 1)
    
    def create_lava_platform(self):
        """Cria plataforma de lava"""
        # Base vermelha escura
        lava_base = (139, 0, 0)
        pygame.draw.rect(self.image, lava_base, (0, 0, self.width, self.height))
        
        # Lava brilhante no topo
        lava_glow = (255, 69, 0)
        pygame.draw.rect(self.image, lava_glow, (0, 0, self.width, 8))
        
        # Efeito de borbulhamento (será animado)
        for i in range(0, self.width, 15):
            bubble_color = (255, 140, 0)
            pygame.draw.circle(self.image, bubble_color, (i + 7, 4), 3)
        
        # Bordas escuras
        pygame.draw.rect(self.image, (100, 0, 0), (0, 0, self.width, self.height), 3)
    
    def setup_platform_properties(self):
        """Configura propriedades específicas do tipo de plataforma"""
        self.friction = 1.0
        self.bounce = 0.0
        self.damage = 0
        self.slippery = False
        self.breakable = False
        
        if self.platform_type == 'ice':
            self.friction = 0.1
            self.slippery = True
        elif self.platform_type == 'cloud':
            self.bounce = 0.3
        elif self.platform_type == 'lava':
            self.damage = 1
        elif self.platform_type == 'wood':
            self.friction = 0.8
    
    def update(self):
        """Atualização da plataforma"""
        self.animation_timer += 1
        
        # Animações específicas por tipo
        if self.platform_type == 'lava':
            self.animate_lava()
        elif self.platform_type == 'cloud':
            self.animate_cloud()
        elif self.platform_type == 'ice':
            self.animate_ice()
    
    def animate_lava(self):
        """Anima a plataforma de lava"""
        if self.animation_timer % 20 == 0:  # Atualiza a cada 20 frames
            # Recria o efeito de borbulhamento
            self.create_lava_platform()
            
            # Adiciona brilho variável
            glow_intensity = abs(math.sin(self.animation_timer * 0.1)) * 50
            glow_surface = pygame.Surface((self.width, 8), pygame.SRCALPHA)
            glow_color = (255, 100, 0, int(glow_intensity))
            glow_surface.fill(glow_color)
            self.image.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_ADD)
    
    def animate_cloud(self):
        """Anima a plataforma de nuvem"""
        # Efeito de flutuação suave
        if self.animation_timer % 120 == 0:  # A cada 2 segundos
            self.create_cloud_platform()
            
            # Adiciona brilho sutil
            alpha_variation = abs(math.sin(self.animation_timer * 0.05)) * 30
            self.image.set_alpha(int(200 + alpha_variation))
    
    def animate_ice(self):
        """Anima a plataforma de gelo"""
        if self.animation_timer % 60 == 0:  # A cada segundo
            # Efeito de cristalização
            sparkle_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            # Adiciona pequenos brilhos aleatórios
            import random
            for _ in range(3):
                x = random.randint(5, self.width - 5)
                y = random.randint(5, self.height - 5)
                sparkle_color = (255, 255, 255, 200)
                pygame.draw.circle(sparkle_surface, sparkle_color, (x, y), 2)
            
            self.image.blit(sparkle_surface, (0, 0), special_flags=pygame.BLEND_ADD)
    
    def draw_effects(self, surface, camera_offset=(0, 0)):
        """Desenha efeitos especiais da plataforma"""
        if self.platform_type == 'lava':
            self.draw_lava_glow(surface, camera_offset)
        elif self.platform_type == 'ice':
            self.draw_ice_shimmer(surface, camera_offset)
    
    def draw_lava_glow(self, surface, camera_offset):
        """Desenha brilho da lava"""
        glow_intensity = abs(math.sin(self.animation_timer * 0.1)) * 100
        glow_height = 20
        
        glow_surface = pygame.Surface((self.width, glow_height), pygame.SRCALPHA)
        
        for i in range(glow_height):
            alpha = int(glow_intensity * (1 - i / glow_height))
            if alpha > 0:
                color = (255, 69, 0, alpha)
                pygame.draw.line(glow_surface, color, (0, i), (self.width, i))
        
        glow_rect = glow_surface.get_rect()
        glow_rect.bottomleft = (self.rect.x + camera_offset[0], self.rect.y + camera_offset[1])
        surface.blit(glow_surface, glow_rect, special_flags=pygame.BLEND_ADD)
    
    def draw_ice_shimmer(self, surface, camera_offset):
        """Desenha brilho do gelo"""
        shimmer_intensity = abs(math.sin(self.animation_timer * 0.08)) * 80
        
        shimmer_surface = pygame.Surface((self.width, 5), pygame.SRCALPHA)
        shimmer_color = (255, 255, 255, int(shimmer_intensity))
        shimmer_surface.fill(shimmer_color)
        
        shimmer_rect = shimmer_surface.get_rect()
        shimmer_rect.topleft = (self.rect.x + camera_offset[0], self.rect.y + camera_offset[1])
        surface.blit(shimmer_surface, shimmer_rect, special_flags=pygame.BLEND_ADD)

class MovingPlatform(Platform):
    """Plataforma que se move com física avançada"""
    
    def __init__(self, x, y, width, height, start_pos, end_pos, speed=2, platform_type='normal'):
        super().__init__(x, y, width, height, platform_type)
        
        self.start_pos = pygame.math.Vector2(start_pos)
        self.end_pos = pygame.math.Vector2(end_pos)
        self.base_speed = speed
        self.current_speed = 0
        self.direction = 1
        self.position = pygame.math.Vector2(x, y)
        
        # Física avançada
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = 0.1
        self.deceleration = 0.95
        self.max_speed = speed
        
        # Calcula a direção do movimento
        self.move_direction = (self.end_pos - self.start_pos).normalize()
        
        # Estados de movimento
        self.state = 'accelerating'  # accelerating, moving, decelerating
        self.pause_timer = 0
        self.pause_duration = 60  # Pausa nos pontos finais
        
    def update(self):
        """Atualiza movimento da plataforma com física suave"""
        super().update()
        
        # Atualiza física do movimento
        self.update_movement_physics()
        
        # Move a plataforma
        self.position += self.velocity
        
        # Verifica chegada aos pontos finais
        self.check_endpoints()
        
        # Atualiza posição do rect
        self.rect.center = (int(self.position.x), int(self.position.y))
    
    def update_movement_physics(self):
        """Atualiza física do movimento com aceleração suave"""
        if self.pause_timer > 0:
            # Pausa nos pontos finais
            self.pause_timer -= 1
            self.velocity *= self.deceleration
            return
        
        # Calcula velocidade alvo
        target_velocity = self.move_direction * self.max_speed * self.direction
        
        # Determina estado baseado na distância aos pontos finais
        distance_to_end = self.position.distance_to(self.end_pos if self.direction == 1 else self.start_pos)
        
        if distance_to_end < 50:  # Próximo ao destino
            self.state = 'decelerating'
            # Reduz velocidade gradualmente
            decel_factor = distance_to_end / 50
            target_velocity *= decel_factor
        elif self.velocity.length() < self.max_speed * 0.9:
            self.state = 'accelerating'
        else:
            self.state = 'moving'
        
        # Aplica aceleração em direção à velocidade alvo
        if self.state == 'accelerating':
            accel_factor = self.acceleration
        elif self.state == 'decelerating':
            accel_factor = self.acceleration * 0.5
        else:
            accel_factor = self.acceleration * 0.2
        
        # Interpola suavemente para a velocidade alvo
        self.velocity = self.velocity.lerp(target_velocity, accel_factor)
    
    def check_endpoints(self):
        """Verifica se chegou aos pontos finais"""
        if self.direction == 1:
            # Indo para o ponto final
            if self.position.distance_to(self.end_pos) < 10:
                self.direction = -1
                self.pause_timer = self.pause_duration
                self.position = self.end_pos.copy()
        else:
            # Voltando para o ponto inicial
            if self.position.distance_to(self.start_pos) < 10:
                self.direction = 1
                self.pause_timer = self.pause_duration
                self.position = self.start_pos.copy()
    
    def get_velocity(self):
        """Retorna a velocidade atual da plataforma (para jogadores que estão em cima)"""
        return self.velocity

class DisappearingPlatform(Platform):
    """Plataforma que desaparece quando pisada"""
    
    def __init__(self, x, y, width, height, delay=60, platform_type='cloud'):
        super().__init__(x, y, width, height, platform_type)
        
        self.delay = delay
        self.timer = 0
        self.triggered = False
        self.original_alpha = 255
        self.respawn_timer = 0
        self.respawn_delay = 300  # 5 segundos
        
    def trigger(self):
        """Ativa o desaparecimento da plataforma"""
        if not self.triggered:
            self.triggered = True
            self.timer = self.delay
    
    def update(self):
        """Atualiza o desaparecimento"""
        super().update()
        
        if self.triggered and self.timer > 0:
            self.timer -= 1
            
            # Efeito de desaparecimento gradual
            alpha = int(self.original_alpha * (self.timer / self.delay))
            self.image.set_alpha(alpha)
            
            # Efeito de tremor
            if self.timer < 20:
                import random
                self.rect.x += random.randint(-2, 2)
                self.rect.y += random.randint(-1, 1)
            
            if self.timer <= 0:
                # Plataforma desapareceu
                self.image.set_alpha(0)
                self.respawn_timer = self.respawn_delay
        
        elif self.respawn_timer > 0:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                # Respawn da plataforma
                self.triggered = False
                self.timer = 0
                self.image.set_alpha(self.original_alpha)

class BouncePlatform(Platform):
    """Plataforma que impulsiona o jogador para cima"""
    
    def __init__(self, x, y, width, height, bounce_strength=25):
        super().__init__(x, y, width, height, 'cloud')
        
        self.bounce_strength = bounce_strength
        self.bounce_timer = 0
        self.activated = False
        
        # Visual especial para plataforma de impulso
        self.create_bounce_visual()
    
    def create_bounce_visual(self):
        """Cria visual especial para plataforma de impulso"""
        super().create_cloud_platform()
        
        # Adiciona setas para indicar impulso
        arrow_color = (0, 255, 0)
        center_x = self.width // 2
        
        # Desenha setas para cima
        for i in range(3):
            y_offset = 5 + i * 8
            arrow_size = 8 - i * 2
            
            # Seta para cima
            points = [
                (center_x, y_offset - arrow_size),
                (center_x - arrow_size, y_offset),
                (center_x + arrow_size, y_offset)
            ]
            pygame.draw.polygon(self.image, arrow_color, points)
    
    def activate_bounce(self):
        """Ativa o efeito de impulso"""
        self.activated = True
        self.bounce_timer = 20  # Duração do efeito visual
    
    def update(self):
        """Atualiza a plataforma de impulso"""
        super().update()
        
        if self.bounce_timer > 0:
            self.bounce_timer -= 1
            
            # Efeito visual de ativação
            if self.bounce_timer % 4 < 2:  # Pisca
                glow_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                glow_surface.fill((0, 255, 0, 100))
                self.image.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_ADD)
            
            if self.bounce_timer <= 0:
                self.activated = False
                self.create_bounce_visual()  # Restaura visual normal
