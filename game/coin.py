import pygame
import math
from game.settings import *
from game.utils import load_image

class Coin(pygame.sprite.Sprite):
    """Classe das moedas coletáveis"""
    
    def __init__(self, x, y, value=COIN_VALUE):
        super().__init__()
        
        # Carregamento das imagens com tamanho correto
        self.load_images()
        
        # Configurações iniciais
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        
        # Valor da moeda
        self.value = value
        
        # Animação
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = COIN_ANIMATION_SPEED
        
        # Efeitos visuais melhorados
        self.float_offset = 0
        self.float_speed = 0.05
        self.original_y = y
        self.pulse_timer = 0
        self.rotation_angle = 0
        self.glow_intensity = 0
        
        # Estados
        self.collected = False
        self.collection_timer = 0
        
    def load_images(self):
        """Carrega as imagens da moeda com tamanho correto"""
        base_image = load_image(COIN_IMAGE, scale=(COIN_SIZE, COIN_SIZE))
        self.images = [base_image]
        
        # Pode adicionar mais frames de animação aqui se tiver
        # self.images.append(load_image('assets/images/coin2.png'))
        
    def update(self):
        """Atualização principal da moeda"""
        if self.collected:
            self.update_collection_effect()
            return
            
        self.update_animation()
        self.update_floating()
        self.update_rotation()
        self.update_pulse()
        self.update_glow()
        self.update_mask()
    
    def update_animation(self):
        """Atualiza a animação da moeda"""
        self.animation_timer += 1
        
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % len(self.images)
            self.image = self.images[self.animation_frame]
    
    def update_floating(self):
        """Atualiza o efeito de flutuação suave"""
        self.float_offset += self.float_speed
        float_y = self.original_y + math.sin(self.float_offset) * 5
        self.rect.y = int(float_y)
    
    def update_rotation(self):
        """Atualiza rotação sutil da moeda"""
        self.rotation_angle += 2
        if self.rotation_angle >= 360:
            self.rotation_angle = 0
        
        # Aplica rotação sutil
        if self.rotation_angle % 10 == 0:  # Rotaciona a cada 10 graus para performance
            rotated_image = pygame.transform.rotate(self.images[self.animation_frame], self.rotation_angle)
            old_center = self.rect.center
            self.image = rotated_image
            self.rect = self.image.get_rect(center=old_center)
    
    def update_pulse(self):
        """Atualiza o efeito de pulsação/brilho"""
        self.pulse_timer += 1
        
        # Efeito de brilho suave
        pulse_value = abs(math.sin(self.pulse_timer * 0.1))
        alpha = int(180 + 75 * pulse_value)
        self.image.set_alpha(alpha)
        
        # Efeito de escala sutil
        if self.pulse_timer % 180 == 0:  # A cada 3 segundos
            scale_factor = 1.2
            original_center = self.rect.center
            scaled_image = pygame.transform.scale(
                self.images[self.animation_frame], 
                (int(COIN_SIZE * scale_factor), int(COIN_SIZE * scale_factor))
            )
            self.image = scaled_image
            self.rect = self.image.get_rect(center=original_center)
            
            # Volta ao tamanho normal após alguns frames
            pygame.time.set_timer(pygame.USEREVENT + 1, 150)
    
    def update_glow(self):
        """Atualiza intensidade do brilho"""
        self.glow_intensity = abs(math.sin(self.pulse_timer * 0.08)) * 100
    
    def update_collection_effect(self):
        """Atualiza o efeito de coleta da moeda"""
        self.collection_timer += 1
        
        # Efeito de subida e rotação rápida
        self.rect.y -= 4
        self.rotation_angle += 15
        
        # Efeito de escala crescente
        scale_factor = 1 + (self.collection_timer * 0.05)
        scaled_image = pygame.transform.scale(
            self.images[0],
            (int(COIN_SIZE * scale_factor), int(COIN_SIZE * scale_factor))
        )
        self.image = scaled_image
        
        # Desaparecimento gradual
        alpha = max(0, 255 - (self.collection_timer * 12))
        self.image.set_alpha(alpha)
        
        # Remove a moeda após o efeito
        if self.collection_timer >= 25:
            self.kill()
    
    def update_mask(self):
        """Atualiza a máscara de colisão"""
        self.mask = pygame.mask.from_surface(self.image)
    
    def collect(self):
        """Marca a moeda como coletada"""
        if not self.collected:
            self.collected = True
            self.collection_timer = 0
            return self.value
        return 0
    
    def draw_glow_effect(self, surface, camera_offset=(0, 0)):
        """Desenha um efeito de brilho melhorado ao redor da moeda"""
        if not self.collected:
            # Cria múltiplas camadas de brilho
            glow_size = COIN_SIZE + 20
            
            # Brilho externo
            outer_glow = pygame.Surface((glow_size + 10, glow_size + 10), pygame.SRCALPHA)
            outer_alpha = int(self.glow_intensity * 0.3)
            for i in range(5):
                radius = (glow_size + 10) // 2 - i * 2
                color = (*GOLD[:3], max(0, outer_alpha - i * 10))
                pygame.draw.circle(outer_glow, color, (outer_glow.get_width() // 2, outer_glow.get_height() // 2), radius)
            
            # Brilho interno
            inner_glow = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            inner_alpha = int(self.glow_intensity * 0.6)
            for i in range(3):
                radius = glow_size // 2 - i * 3
                color = (*YELLOW[:3], max(0, inner_alpha - i * 20))
                pygame.draw.circle(inner_glow, color, (inner_glow.get_width() // 2, inner_glow.get_height() // 2), radius)
            
            # Posiciona os brilhos
            outer_rect = outer_glow.get_rect(center=(
                self.rect.centerx + camera_offset[0], 
                self.rect.centery + camera_offset[1]
            ))
            inner_rect = inner_glow.get_rect(center=(
                self.rect.centerx + camera_offset[0], 
                self.rect.centery + camera_offset[1]
            ))
            
            surface.blit(outer_glow, outer_rect, special_flags=pygame.BLEND_ADD)
            surface.blit(inner_glow, inner_rect, special_flags=pygame.BLEND_ADD)
    
    def draw_sparkles(self, surface, camera_offset=(0, 0)):
        """Desenha pequenas estrelas ao redor da moeda"""
        if not self.collected:
            import random
            
            # Gera sparkles aleatórios
            for i in range(3):
                angle = (self.pulse_timer + i * 120) % 360
                distance = 30 + math.sin(self.pulse_timer * 0.05 + i) * 10
                
                sparkle_x = self.rect.centerx + math.cos(math.radians(angle)) * distance + camera_offset[0]
                sparkle_y = self.rect.centery + math.sin(math.radians(angle)) * distance + camera_offset[1]
                
                # Desenha estrela pequena
                sparkle_size = 3 + int(abs(math.sin(self.pulse_timer * 0.1 + i)) * 2)
                sparkle_color = YELLOW if i % 2 == 0 else WHITE
                
                # Desenha cruz para formar estrela
                pygame.draw.line(surface, sparkle_color, 
                               (sparkle_x - sparkle_size, sparkle_y), 
                               (sparkle_x + sparkle_size, sparkle_y), 2)
                pygame.draw.line(surface, sparkle_color, 
                               (sparkle_x, sparkle_y - sparkle_size), 
                               (sparkle_x, sparkle_y + sparkle_size), 2)

class PowerUpCoin(Coin):
    """Moeda especial com valor maior e efeitos visuais intensos"""
    
    def __init__(self, x, y):
        super().__init__(x, y, value=COIN_VALUE * 5)
        
        # Efeitos visuais mais intensos
        self.float_speed = 0.08
        self.animation_speed = COIN_ANIMATION_SPEED // 2
        
        # Aplica cor dourada mais intensa
        gold_overlay = pygame.Surface((COIN_SIZE, COIN_SIZE), pygame.SRCALPHA)
        gold_overlay.fill((*GOLD[:3], 100))
        for i, image in enumerate(self.images):
            enhanced_image = image.copy()
            enhanced_image.blit(gold_overlay, (0, 0), special_flags=pygame.BLEND_ADD)
            self.images[i] = enhanced_image
    
    def draw_glow_effect(self, surface, camera_offset=(0, 0)):
        """Efeito de brilho mais intenso para moeda especial"""
        super().draw_glow_effect(surface, camera_offset)
        
        if not self.collected:
            # Brilho adicional dourado
            extra_glow_size = COIN_SIZE + 30
            extra_glow = pygame.Surface((extra_glow_size, extra_glow_size), pygame.SRCALPHA)
            
            # Múltiplos anéis de brilho dourado
            for i in range(4):
                radius = extra_glow_size // 2 - i * 5
                alpha = int(self.glow_intensity * 0.4 - i * 15)
                if alpha > 0:
                    color = (*GOLD[:3], alpha)
                    pygame.draw.circle(extra_glow, color, 
                                     (extra_glow.get_width() // 2, extra_glow.get_height() // 2), 
                                     radius)
            
            extra_rect = extra_glow.get_rect(center=(
                self.rect.centerx + camera_offset[0], 
                self.rect.centery + camera_offset[1]
            ))
            surface.blit(extra_glow, extra_rect, special_flags=pygame.BLEND_ADD)

class BonusCoin(Coin):
    """Moeda bônus temporária com efeitos especiais"""
    
    def __init__(self, x, y, lifetime=600):  # 10 segundos a 60 FPS
        super().__init__(x, y, value=COIN_VALUE * 2)
        self.lifetime = lifetime
        self.spawn_timer = 0
        self.max_lifetime = lifetime
        
        # Aplica cor prateada
        silver_overlay = pygame.Surface((COIN_SIZE, COIN_SIZE), pygame.SRCALPHA)
        silver_overlay.fill((200, 200, 255, 80))
        for i, image in enumerate(self.images):
            enhanced_image = image.copy()
            enhanced_image.blit(silver_overlay, (0, 0), special_flags=pygame.BLEND_ADD)
            self.images[i] = enhanced_image
        
    def update(self):
        """Atualização com tempo de vida limitado"""
        super().update()
        
        if not self.collected:
            self.spawn_timer += 1
            
            # Efeito de urgência - pisca mais rápido conforme o tempo passa
            urgency_threshold = self.lifetime - 180  # Últimos 3 segundos
            if self.spawn_timer > urgency_threshold:
                flash_speed = max(5, 20 - (self.spawn_timer - urgency_threshold) // 10)
                if (self.spawn_timer // flash_speed) % 2:
                    self.image.set_alpha(100)
                else:
                    self.image.set_alpha(255)
            
            # Remove após o tempo limite
            if self.spawn_timer >= self.lifetime:
                self.kill()
    
    def draw_glow_effect(self, surface, camera_offset=(0, 0)):
        """Efeito de brilho prateado para moeda bônus"""
        if not self.collected:
            # Calcula intensidade baseada no tempo restante
            time_ratio = 1 - (self.spawn_timer / self.max_lifetime)
            intensity = self.glow_intensity * time_ratio
            
            glow_size = COIN_SIZE + 15
            bonus_glow = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            
            # Brilho prateado/azulado
            for i in range(3):
                radius = glow_size // 2 - i * 3
                alpha = int(intensity * 0.5 - i * 10)
                if alpha > 0:
                    color = (200, 200, 255, alpha)
                    pygame.draw.circle(bonus_glow, color, 
                                     (bonus_glow.get_width() // 2, bonus_glow.get_height() // 2), 
                                     radius)
            
            bonus_rect = bonus_glow.get_rect(center=(
                self.rect.centerx + camera_offset[0], 
                self.rect.centery + camera_offset[1]
            ))
            surface.blit(bonus_glow, bonus_rect, special_flags=pygame.BLEND_ADD)
