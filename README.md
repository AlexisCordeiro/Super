# 🦸 Super Hero - Jogo de Plataforma

Um jogo de plataforma completo desenvolvido em Python com Pygame, inspirado no clássico Super Mario, com gráficos modernos, física realista e múltiplos níveis desafiadores.

## 🎮 Características do Jogo

### 🎯 Gameplay
- **3 níveis únicos** com dificuldade crescente
- **Sistema de física realista** com gravidade e colisões precisas
- **Personagem principal** com animações fluidas e controles responsivos
- **Inimigos inteligentes** com IA avançada e diferentes comportamentos
- **Sistema de coleta** com múltiplos tipos de moedas
- **Plataformas interativas** com propriedades especiais

### 🎨 Visual e Interface
- **Interface moderna** com elementos visuais avançados
- **Sistema de partículas** para efeitos especiais
- **Câmera dinâmica** que segue o jogador suavemente
- **Animações controladas** - personagem fica parado quando não se move
- **Efeitos visuais** baseados no estado do personagem
- **HUD informativo** com vida, pontuação e tempo

### 🕹️ Controles
- **WASD** ou **Setas**: Movimento
- **Espaço**: Pular
- **X**: Atacar
- **ESC**: Pausar
- **Enter**: Selecionar no menu

## 🏗️ Arquitetura do Código

### 📁 Estrutura do Projeto
```
super-hero/
├── main.py                 # Arquivo principal
├── game/                   # Pacote do jogo
│   ├── __init__.py
│   ├── settings.py         # Configurações centralizadas
│   ├── utils.py           # Funções utilitárias
│   ├── game_manager.py    # Gerenciador principal
│   ├── player.py          # Classe do jogador
│   ├── enemy.py           # Classe dos inimigos
│   ├── coin.py            # Sistema de moedas
│   └── platform.py        # Sistema de plataformas
├── assets/                # Recursos do jogo
│   ├── images/            # Imagens
│   └── sounds/            # Sons
├── venv/                  # Ambiente virtual
└── README.md              # Este arquivo
```

### 🛠️ Classes Principais

#### `GameManager`
- Gerencia estados do jogo (menu, jogando, pausado, game over)
- Controla níveis e progressão
- Gerencia sprites e colisões
- Interface moderna com painéis e botões estilizados

#### `Player`
- **Sistema de animação controlado**: 5 estados (IDLE, WALKING, JUMPING, FALLING, ATTACKING)
- **Física realista** com detecção precisa de colisões
- **Efeitos visuais**: partículas de poeira, trilha de movimento, efeito de pouso
- **Sistema de vida** com invulnerabilidade temporária

#### `Enemy`
- **IA inteligente** com estados: patrulha, perseguição, ataque
- **Sistema de detecção** do jogador com alcance configurável
- **Comportamentos variados**: patrulhamento, alerta, combate
- **Efeitos visuais**: barras de vida, indicadores de estado

#### `Coin` (3 tipos)
- **Coin**: Moeda básica com efeito de flutuação
- **PowerUpCoin**: Vale 5x mais, efeitos intensos
- **BonusCoin**: Vale 2x mais, tempo limitado

#### `Platform` (6 tipos visuais)
- **Normal**: Madeira com textura detalhada
- **Grass**: Terra com grama no topo
- **Stone**: Blocos de pedra individuais
- **Wood**: Tábuas de madeira com veios
- **Ice**: Translúcido com cristais (escorregadio)
- **Cloud**: Múltiplas camadas fofas
- **Lava**: Animada com borbulhamento (causa dano)

#### Plataformas Especiais
- **MovingPlatform**: Move entre pontos definidos
- **DisappearingPlatform**: Desaparece quando pisada
- **BouncePlatform**: Impulsiona o jogador para cima

## 🎯 Funcionalidades Avançadas

### 🎬 Sistema de Animação
- **Estados controlados**: Personagem só anima quando necessário
- **Transições suaves** entre diferentes animações
- **Efeitos baseados no movimento**: balanço na caminhada, inclinação no pulo

### 🌟 Efeitos Visuais
- **Sistema de partículas** para poeira e efeitos especiais
- **Trilha de movimento** que segue o jogador
- **Efeitos de pouso** com ondas de impacto
- **Brilho e shimmer** em elementos especiais

### 🧠 Inteligência Artificial
- **Detecção inteligente** do jogador pelos inimigos
- **Estados comportamentais** com transições naturais
- **Patrulhamento dinâmico** com pausas aleatórias

### 📱 Interface Moderna
- **Botões com estados** (hover, pressed)
- **Painéis semi-transparentes** com cantos arredondados
- **Barras de progresso** e vida com gradientes
- **Ícones informativos** com texto

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7+
- Pygame

### Instalação
1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install pygame
   ```
4. Execute o jogo:
   ```bash
   python main.py
   ```

## 🎮 Níveis do Jogo

### 🌱 Nível 1: Básico
- Introdução aos controles
- Plataformas simples
- Poucos inimigos
- Moedas básicas

### ⚡ Nível 2: Intermediário
- Plataformas de gelo (escorregadias)
- Plataformas móveis
- Inimigos mais inteligentes
- Lacunas no chão

## 🏆 Sistema de Pontuação
- **Moedas normais**: 10 pontos
- **PowerUp Coins**: 50 pontos
- **Bonus Coins**: 20 pontos
- **Derrotar inimigos**: 25 pontos
- **Completar nível**: 100 pontos

## 🎨 Recursos Visuais
- **Dimensões otimizadas**: Personagens 64x96px, inimigos 60x90px
- **Moedas**: 32px com animações fluidas
- **Tela**: 1280x720 para melhor experiência visual
- **Mundo expandido**: 4000px de largura para exploração

## 🔧 Configurações Técnicas
- **FPS**: 60 para jogabilidade suave
- **Física**: Gravidade 0.8, força de pulo -16
- **Velocidades**: Jogador 6px/frame, inimigos 2px/frame
- **Invulnerabilidade**: 2 segundos após tomar dano

## 🎵 Assets Necessários
O jogo utiliza os seguintes arquivos de assets:
- `assets/images/pparado.png` - Jogador parado
- `assets/images/pandando.png` - Jogador andando
- `assets/images/ppulando.png` - Jogador pulando
- `assets/images/patacando.png` - Jogador atacando
- `assets/images/vparado.png` - Inimigo parado
- `assets/images/vandando.png` - Inimigo andando
- `assets/images/vatacando.png` - Inimigo atacando
- `assets/images/vsofrendo.png` - Inimigo sofrendo dano
- `assets/images/coin.png` - Moeda
- `assets/images/cenario.jpg` - Cenário de fundo

## 🐛 Resolução de Problemas
- **Erro de módulo não encontrado**: Certifique-se de que o pygame está instalado
- **Imagens não carregam**: Verifique se os arquivos estão na pasta `assets/images/`
- **Performance baixa**: Ajuste o FPS nas configurações

## 🤝 Contribuições
Este é um projeto educacional demonstrando:
- Arquitetura de jogos em Python
- Programação orientada a objetos
- Sistemas de física e colisão
- Interface de usuário moderna
- Otimização de performance

## 📝 Licença
Projeto desenvolvido para fins educacionais e demonstração de técnicas de desenvolvimento de jogos.

---

**Desenvolvido com ❤️ usando Python e Pygame** 
