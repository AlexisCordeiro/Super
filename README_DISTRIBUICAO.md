# 🎮 Super Hero - Distribuição do Jogo

## 📦 Arquivos Gerados

O PyInstaller criou os seguintes arquivos na pasta `dist/`:

### 🍎 Para macOS:
- **`SuperHero.app`** - App bundle completo para macOS
- **`SuperHero`** - Executável simples (21MB)

## 🚀 Como Distribuir

### Para Usuários Mac:
1. **Recomendado**: Compartilhe o arquivo `SuperHero.app`
   - É um app bundle completo
   - Funciona como qualquer aplicativo do macOS
   - Duplo clique para executar
   - Pode ser movido para a pasta Applications

2. **Alternativo**: Compartilhe o executável `SuperHero`
   - Arquivo único de 21MB
   - Execute no terminal ou duplo clique

### Para Outros Sistemas:
Se quiser criar executáveis para Windows ou Linux, execute:

```bash
# Para Windows (no Windows ou usando Wine)
pyinstaller --onefile --windowed main.py

# Para Linux
pyinstaller --onefile main.py
```

## 🎯 Características do Executável

✅ **Incluído no executável:**
- Todas as imagens da pasta `assets/images/`
- Todos os sons da pasta `assets/sounds/`
- Todo o código Python do jogo
- Bibliotecas necessárias (pygame, etc.)

✅ **Funciona sem instalação:**
- Não precisa instalar Python
- Não precisa instalar pygame
- Não precisa instalar dependências

## 🎮 Como Jogar

### Controles:
- **WASD** ou **Setas** - Mover
- **ESPAÇO** - Pular
- **X** - Atacar
- **ESC** - Pausar/Menu

### Objetivo:
- Complete as 2 fases do jogo
- Colete moedas para aumentar a pontuação
- Derrote inimigos
- Chegue ao final de cada nível

## 🔧 Informações Técnicas

- **Tamanho**: ~21MB
- **Plataforma**: macOS (ARM64/Intel)
- **Dependências**: Nenhuma (tudo incluído)
- **Versão**: 1.0.0

## 📋 Resolução de Problemas

### Se o jogo não iniciar:
1. Verifique se tem permissão para executar
2. No macOS, pode precisar autorizar em "Preferências do Sistema > Segurança"
3. Tente executar pelo terminal: `./SuperHero`

### Se faltar assets:
- O executável deve incluir tudo automaticamente
- Se houver problemas, verifique se a pasta `assets/` estava presente durante a compilação

## 🎉 Parabéns!

Seu jogo Super Hero agora está pronto para distribuição! 🚀

### Próximos Passos:
1. Teste o executável em diferentes Macs
2. Considere criar um instalador (.dmg)
3. Adicione um ícone personalizado
4. Publique em plataformas como itch.io

---

**Desenvolvido com ❤️ usando Python e Pygame** 