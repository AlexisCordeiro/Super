#!/usr/bin/env python3
"""
Super Hero - Jogo de Plataforma
Um jogo de plataforma estilo Super Mario com personagens, inimigos, moedas e obstáculos.

Controles:
- WASD ou Setas: Movimento
- Espaço: Pular
- X: Atacar
- ESC: Pausar
- Enter: Selecionar no menu

Recursos:
- 3 níveis únicos com dificuldade crescente
- Sistema de física realista
- Diferentes tipos de plataformas (gelo, lava, nuvem, etc.)
- Múltiplos tipos de moedas
- Inimigos inteligentes com IA
- Interface moderna
- Sistema de partículas e efeitos visuais
- Câmera suave
- Sistema de pontuação e vidas
"""

import pygame
import sys
import os

# Adiciona o diretório do jogo ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.game_manager import GameManager

def main():
    """Função principal do jogo"""
    try:
        # Inicializa o gerenciador do jogo
        game = GameManager()
        
        # Executa o loop principal
        game.run()
        
    except KeyboardInterrupt:
        print("\nJogo interrompido pelo usuário.")
    except Exception as e:
        print(f"Erro durante a execução do jogo: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Garante que o Pygame seja finalizado
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("=" * 60)
    print("🦸 SUPER HERO - JOGO DE PLATAFORMA 🦸")
    print("=" * 60)
    print("Inicializando o jogo...")
    print("Pressione ESC para pausar durante o jogo")
    print("Use WASD ou setas para mover, ESPAÇO para pular, X para atacar")
    print("=" * 60)
    
    main()
