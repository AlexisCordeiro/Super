#!/bin/bash

# Script para executar o jogo Super Hero

echo "🎮 Iniciando Super Hero..."

# Verifica se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativa o ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instala dependências se necessário
echo "📥 Verificando dependências..."
pip install -r requirements.txt

# Executa o jogo
echo "🚀 Iniciando o jogo..."
python3 main.py

# Desativa o ambiente virtual
deactivate

echo "👋 Obrigado por jogar!" 