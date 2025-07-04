# Utilitários do jogo
import pygame
import os
import math
from game.settings import *

def load_image(path, size=None, scale=None):
    """Carrega uma imagem com opções de redimensionamento preservando transparência"""
    try:
        # Carrega a imagem original
        image = pygame.image.load(path)
        
        # Verifica se a imagem tem canal alpha
        if image.get_flags() & pygame.SRCALPHA or image.get_bitsize() == 32:
            # Converte preservando alpha
            image = image.convert_alpha()
        else:
            # Converte normalmente se não tiver alpha
            image = image.convert()
        
        # Redimensiona se necessário
        if size or scale:
            if size:
                # Se size for uma tupla, usa diretamente
                if isinstance(size, tuple):
                    target_size = size
                else:
                    # Se size for um número, cria uma tupla quadrada
                    target_size = (size, size)
            elif scale:
                # Se scale for uma tupla, usa como size
                if isinstance(scale, tuple):
                    target_size = scale
                else:
                    # Se scale for um número, aplica proporcionalmente
                    current_size = image.get_size()
                    target_size = (int(current_size[0] * scale), int(current_size[1] * scale))
            
            # Redimensiona preservando transparência
            if image.get_flags() & pygame.SRCALPHA:
                # Cria nova superfície com alpha
                scaled_image = pygame.Surface(target_size, pygame.SRCALPHA, 32)
                scaled_image = scaled_image.convert_alpha()
                
                # Redimensiona usando smoothscale para melhor qualidade
                try:
                    scaled_image = pygame.transform.smoothscale(image, target_size)
                except:
                    # Fallback para scale normal se smoothscale falhar
                    scaled_image = pygame.transform.scale(image, target_size)
                
                # Garante que mantém o canal alpha
                if not (scaled_image.get_flags() & pygame.SRCALPHA):
                    temp_surface = pygame.Surface(target_size, pygame.SRCALPHA, 32)
                    temp_surface = temp_surface.convert_alpha()
                    temp_surface.blit(scaled_image, (0, 0))
                    scaled_image = temp_surface
                
                image = scaled_image
            else:
                # Redimensiona normalmente se não tiver alpha
                image = pygame.transform.scale(image, target_size)
        
        return image
        
    except pygame.error as e:
        print(f"❌ Erro ao carregar imagem {path}: {e}")
        # Retorna uma imagem de placeholder com transparência
        if size:
            if isinstance(size, tuple):
                placeholder_size = size
            else:
                placeholder_size = (size, size)
        elif scale and isinstance(scale, tuple):
            placeholder_size = scale
        else:
            placeholder_size = (64, 64)
            
        placeholder = pygame.Surface(placeholder_size, pygame.SRCALPHA, 32)
        placeholder = placeholder.convert_alpha()
        placeholder.fill((255, 0, 255, 128))  # Rosa transparente
        return placeholder

def load_sound(path, volume=1.0):
    """
    Carrega um som com volume específico
    """
    try:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        return sound
    except pygame.error as e:
        print(f"Erro ao carregar som {path}: {e}")
        return None

def scale_image_smart(image, target_size, maintain_aspect=True):
    """
    Redimensiona uma imagem de forma inteligente
    """
    if maintain_aspect:
        # Calcula escala mantendo proporção
        scale_x = target_size[0] / image.get_width()
        scale_y = target_size[1] / image.get_height()
        scale = min(scale_x, scale_y)
        
        new_width = int(image.get_width() * scale)
        new_height = int(image.get_height() * scale)
        
        return pygame.transform.scale(image, (new_width, new_height))
    else:
        return pygame.transform.scale(image, target_size)

def draw_text(screen, text, size, x, y, color, font=None):
    """Desenha texto centralizado"""
    if font is None:
        font = pygame.font.Font(None, size)
    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_text_left(screen, text, size, x, y, color, font=None):
    """Desenha texto alinhado à esquerda"""
    if font is None:
        font = pygame.font.Font(None, size)
    text_surface = font.render(str(text), True, color)
    screen.blit(text_surface, (x, y))

def draw_text_right(screen, text, size, x, y, color, font=None):
    """Desenha texto alinhado à direita"""
    if font is None:
        font = pygame.font.Font(None, size)
    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect()
    text_rect.right = x
    text_rect.y = y
    screen.blit(text_surface, text_rect)

def draw_gradient_rect(surface, rect, color1, color2, vertical=True):
    """
    Desenha um retângulo com gradiente
    """
    if vertical:
        for y in range(rect.height):
            ratio = y / rect.height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(surface, (r, g, b), 
                           (rect.x, rect.y + y), (rect.x + rect.width, rect.y + y))
    else:
        for x in range(rect.width):
            ratio = x / rect.width
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(surface, (r, g, b), 
                           (rect.x + x, rect.y), (rect.x + x, rect.y + rect.height))

def draw_rounded_rect(surface, rect, color, radius=10, border_color=None, border_width=0):
    """
    Desenha um retângulo com cantos arredondados
    """
    # Cria uma superfície temporária
    temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    # Desenha o retângulo arredondado
    pygame.draw.rect(temp_surface, color, (0, 0, rect.width, rect.height), border_radius=radius)
    
    # Desenha borda se especificada
    if border_color and border_width > 0:
        pygame.draw.rect(temp_surface, border_color, (0, 0, rect.width, rect.height), 
                        border_width, border_radius=radius)
    
    # Blita na superfície principal
    surface.blit(temp_surface, rect.topleft)

def draw_health_bar(surface, x, y, width, height, current_health, max_health, 
                   bg_color=DARK_GRAY, health_color=UI_HEALTH_COLOR, border_color=WHITE):
    """
    Desenha uma barra de vida moderna
    """
    # Fundo da barra
    bg_rect = pygame.Rect(x, y, width, height)
    draw_rounded_rect(surface, bg_rect, bg_color, radius=height//2)
    
    # Barra de vida
    if current_health > 0:
        health_width = int((current_health / max_health) * (width - 4))
        health_rect = pygame.Rect(x + 2, y + 2, health_width, height - 4)
        
        # Gradiente na barra de vida
        if current_health / max_health > 0.6:
            color = GREEN
        elif current_health / max_health > 0.3:
            color = YELLOW
        else:
            color = RED
        
        draw_rounded_rect(surface, health_rect, color, radius=(height-4)//2)
    
    # Borda
    pygame.draw.rect(surface, border_color, bg_rect, 2, border_radius=height//2)

def draw_progress_bar(surface, x, y, width, height, progress, 
                     bg_color=DARK_GRAY, fill_color=UI_ACCENT_COLOR, border_color=WHITE):
    """
    Desenha uma barra de progresso moderna
    """
    # Fundo da barra
    bg_rect = pygame.Rect(x, y, width, height)
    draw_rounded_rect(surface, bg_rect, bg_color, radius=height//2)
    
    # Barra de progresso
    if progress > 0:
        progress_width = int(progress * (width - 4))
        progress_rect = pygame.Rect(x + 2, y + 2, progress_width, height - 4)
        draw_rounded_rect(surface, progress_rect, fill_color, radius=(height-4)//2)
    
    # Borda
    pygame.draw.rect(surface, border_color, bg_rect, 2, border_radius=height//2)

def draw_button(surface, rect, text, font, 
               bg_color=DARK_GRAY, text_color=WHITE, border_color=UI_ACCENT_COLOR,
               hover=False, pressed=False):
    """
    Desenha um botão moderno com estados
    """
    # Cor baseada no estado
    if pressed:
        button_color = (bg_color[0] * 0.7, bg_color[1] * 0.7, bg_color[2] * 0.7)
        border_width = 4
    elif hover:
        button_color = (min(255, bg_color[0] * 1.2), min(255, bg_color[1] * 1.2), min(255, bg_color[2] * 1.2))
        border_width = 3
    else:
        button_color = bg_color
        border_width = 2
    
    # Desenha o botão
    draw_rounded_rect(surface, rect, button_color, radius=10, border_color=border_color, border_width=border_width)
    
    # Desenha o texto
    draw_text(surface, text, font.get_height(), rect.centerx, rect.centery, text_color, font)

def draw_panel(surface, rect, bg_color=UI_BG_COLOR, border_color=UI_BORDER_COLOR, alpha=150):
    """
    Desenha um painel semi-transparente moderno
    """
    # Cria superfície com transparência
    panel_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    # Cor com alpha
    if len(bg_color) == 3:
        panel_color = (*bg_color, alpha)
    else:
        panel_color = bg_color
    
    # Desenha o painel
    draw_rounded_rect(panel_surface, pygame.Rect(0, 0, rect.width, rect.height), 
                     panel_color, radius=15)
    
    # Borda
    if border_color:
        pygame.draw.rect(panel_surface, border_color, 
                        pygame.Rect(0, 0, rect.width, rect.height), 2, border_radius=15)
    
    # Blita na superfície principal
    surface.blit(panel_surface, rect.topleft)

def draw_icon_with_text(surface, icon, text, font, x, y, text_color=WHITE, spacing=10):
    """
    Desenha um ícone com texto ao lado
    """
    # Desenha o ícone
    icon_rect = icon.get_rect(topleft=(x, y))
    surface.blit(icon, icon_rect)
    
    # Desenha o texto
    text_x = x + icon.get_width() + spacing
    text_y = y + (icon.get_height() - font.get_height()) // 2
    draw_text_left(surface, text, font.get_height(), text_x, text_y, text_color, font)
    
    return icon_rect.width + spacing + font.size(text)[0]

class Camera:
    """Câmera simples para seguir o jogador"""
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """Aplica o offset da câmera a uma entidade"""
        return entity.rect.move(self.camera.x, self.camera.y)

    def update(self, target):
        """Atualiza a posição da câmera para seguir o alvo"""
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)
        
        # Limita a câmera aos limites do mundo
        x = min(0, x)  # Esquerda
        y = min(0, y)  # Topo
        x = max(-(self.width - SCREEN_WIDTH), x)  # Direita
        y = max(-(self.height - SCREEN_HEIGHT), y)  # Baixo
        
        self.camera = pygame.Rect(x, y, self.width, self.height)

def clamp(value, min_value, max_value):
    """Limita um valor entre min e max"""
    return max(min_value, min(value, max_value))

def lerp(a, b, t):
    """Interpolação linear entre dois valores"""
    return a + (b - a) * t

def distance(pos1, pos2):
    """Calcula distância entre duas posições"""
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return (dx * dx + dy * dy) ** 0.5 

def load_sprite(path, size=None):
    """Carrega um sprite com transparência otimizada especificamente para personagens"""
    try:
        # Carrega a imagem original
        original = pygame.image.load(path)
        
        # Força conversão com alpha
        if original.get_bitsize() == 32 or original.get_masks()[3] != 0:
            # Tem canal alpha
            sprite = original.convert_alpha()
        else:
            # Não tem canal alpha, cria um
            sprite = pygame.Surface(original.get_size(), pygame.SRCALPHA, 32)
            sprite = sprite.convert_alpha()
            sprite.blit(original, (0, 0))
        
        # Redimensiona se necessário
        if size:
            if isinstance(size, tuple):
                target_size = size
            else:
                target_size = (size, size)
            
            # Usa smoothscale para melhor qualidade
            try:
                sprite = pygame.transform.smoothscale(sprite, target_size)
            except:
                sprite = pygame.transform.scale(sprite, target_size)
            
            # Garante que ainda tem alpha após redimensionamento
            if not (sprite.get_flags() & pygame.SRCALPHA):
                temp = pygame.Surface(target_size, pygame.SRCALPHA, 32)
                temp = temp.convert_alpha()
                temp.blit(sprite, (0, 0))
                sprite = temp
        
        return sprite
        
    except Exception as e:
        print(f"❌ Erro ao carregar sprite {path}: {e}")
        # Placeholder com transparência
        size = size if size else (64, 64)
        if not isinstance(size, tuple):
            size = (size, size)
        
        placeholder = pygame.Surface(size, pygame.SRCALPHA, 32)
        placeholder = placeholder.convert_alpha()
        # Desenha um retângulo colorido transparente
        pygame.draw.rect(placeholder, (255, 100, 100, 150), placeholder.get_rect())
        pygame.draw.rect(placeholder, (255, 255, 255, 200), placeholder.get_rect(), 2)
        return placeholder 