#!/bin/bash

# 🎮 Script de Teste do Super Hero
# Este script facilita o teste do jogo em diferentes formatos

echo "🎮 Testando Super Hero..."
echo "========================="

# Verificar se os arquivos existem
if [ ! -f "dist/SuperHero" ]; then
    echo "❌ Executável não encontrado! Execute primeiro: ./build_game.sh"
    exit 1
fi

if [ ! -d "dist/SuperHero.app" ]; then
    echo "❌ App bundle não encontrado! Execute primeiro: ./build_game.sh"
    exit 1
fi

echo "📁 Arquivos encontrados:"
echo "   ✅ dist/SuperHero ($(du -h dist/SuperHero | cut -f1))"
echo "   ✅ dist/SuperHero.app ($(du -h dist/SuperHero.app | cut -f1))"
echo ""

# Menu de opções
echo "🎯 Escolha como testar:"
echo "1) Testar executável simples (./dist/SuperHero)"
echo "2) Testar app bundle (SuperHero.app)"
echo "3) Testar ambos"
echo "4) Verificar dependências"
echo "5) Sair"
echo ""

read -p "Digite sua opção (1-5): " opcao

case $opcao in
    1)
        echo "🚀 Testando executável simples..."
        ./dist/SuperHero
        ;;
    2)
        echo "🚀 Testando app bundle..."
        open dist/SuperHero.app
        ;;
    3)
        echo "🚀 Testando executável simples..."
        ./dist/SuperHero &
        sleep 2
        echo "🚀 Testando app bundle..."
        open dist/SuperHero.app
        ;;
    4)
        echo "🔍 Verificando dependências..."
        echo ""
        echo "📦 Conteúdo do executável:"
        otool -L dist/SuperHero | head -10
        echo ""
        echo "📁 Assets incluídos:"
        ls -la dist/assets/
        ;;
    5)
        echo "👋 Saindo..."
        exit 0
        ;;
    *)
        echo "❌ Opção inválida!"
        exit 1
        ;;
esac

echo ""
echo "🎉 Teste concluído!" 