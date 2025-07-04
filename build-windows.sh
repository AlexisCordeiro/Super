#!/bin/bash

# Script para compilar executável Windows usando Wine no macOS
# AVISO: Este método é experimental e pode não funcionar perfeitamente

echo "🍷 Tentando compilar executável Windows usando Wine..."
echo "⚠️  AVISO: Este método é experimental!"

# Verifica se Wine está instalado
if ! command -v wine &> /dev/null; then
    echo "❌ Wine não está instalado!"
    echo "📦 Instale com: brew install wine"
    echo "🔗 Ou baixe de: https://www.winehq.org/"
    exit 1
fi

# Verifica se Python está instalado no Wine
echo "🔍 Verificando Python no Wine..."
if ! wine python --version &> /dev/null; then
    echo "❌ Python não está instalado no Wine!"
    echo "📦 Baixe Python para Windows e instale via Wine"
    echo "🔗 https://www.python.org/downloads/windows/"
    exit 1
fi

# Instala dependências no Wine
echo "📦 Instalando dependências..."
wine pip install pygame pyinstaller

# Compila o executável
echo "🔨 Compilando executável Windows..."
wine pyinstaller super_hero.spec

# Verifica se foi criado
if [ -f "dist/SuperHero.exe" ]; then
    echo "✅ Executável Windows criado com sucesso!"
    echo "📁 Localização: dist/SuperHero.exe"
    echo "📊 Tamanho: $(ls -lh dist/SuperHero.exe | awk '{print $5}')"
else
    echo "❌ Falha ao criar executável Windows"
    exit 1
fi

echo "🎉 Processo concluído!" 