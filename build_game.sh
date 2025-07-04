#!/bin/bash

# 🎮 Script de Compilação do Super Hero
# Este script automatiza a criação do executável do jogo

echo "🎮 Compilando Super Hero..."
echo "================================"

# Ativar ambiente virtual
echo "📦 Ativando ambiente virtual..."
source venv/bin/activate

# Verificar se PyInstaller está instalado
if ! command -v pyinstaller &> /dev/null; then
    echo "⚠️  PyInstaller não encontrado. Instalando..."
    pip install pyinstaller
fi

# Limpar builds anteriores
echo "🧹 Limpando builds anteriores..."
rm -rf build/
rm -rf dist/

# Compilar o jogo
echo "🔨 Compilando o jogo..."
pyinstaller super_hero.spec

# Verificar se a compilação foi bem-sucedida
if [ -f "dist/SuperHero.app/Contents/MacOS/SuperHero" ]; then
    echo "✅ Compilação concluída com sucesso!"
    echo ""
    echo "📁 Arquivos gerados em:"
    echo "   - dist/SuperHero.app (App Bundle para macOS)"
    echo "   - dist/SuperHero (Executável simples)"
    echo ""
    echo "🎯 Para testar:"
    echo "   open dist/SuperHero.app"
    echo ""
    echo "📦 Para distribuir:"
    echo "   Compartilhe a pasta SuperHero.app"
    echo ""
    
    # Mostrar tamanho dos arquivos
    echo "📊 Tamanhos dos arquivos:"
    du -h dist/SuperHero
    du -h dist/SuperHero.app
    
else
    echo "❌ Erro na compilação!"
    echo "Verifique os logs acima para mais detalhes."
    exit 1
fi

echo "🎉 Processo concluído!" 