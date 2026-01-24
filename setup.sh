#!/bin/bash
# Setup Script - LinkedIn Optimizer Assistant
# Autor: JC | CloserPace
# Versão: 1.0

set -e  # Exit on error

echo "🚀 LinkedIn Optimizer Assistant - Setup"
echo "========================================="
echo ""

# Check Python version
echo "📋 A verificar Python..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "❌ Erro: Python 3.11+ é necessário (encontrado: $python_version)"
    exit 1
fi

echo "✓ Python $python_version OK"
echo ""

# Create virtual environment
echo "📦 A criar virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment criado"
else
    echo "⚠️  Virtual environment já existe"
fi
echo ""

# Activate virtual environment
echo "🔧 A ativar virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  A atualizar pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ pip atualizado"
echo ""

# Install dependencies
echo "📚 A instalar dependências..."
pip install -r requirements.txt
echo "✓ Dependências instaladas"
echo ""

# Create necessary directories
echo "📁 A criar estrutura de pastas..."
mkdir -p data/inputs/exemplos
mkdir -p data/outputs/exemplos
mkdir -p tests/test_modules
echo "✓ Estrutura criada"
echo ""

# Verify installation
echo "🧪 A verificar instalação..."
if python3 src/cli.py info > /dev/null 2>&1; then
    echo "✓ CLI funcional"
else
    echo "❌ Erro ao executar CLI"
    exit 1
fi
echo ""

echo "========================================="
echo "✅ Setup completo!"
echo ""
echo "📖 Próximos passos:"
echo ""
echo "  1. Ativa o virtual environment:"
echo "     $ source venv/bin/activate"
echo ""
echo "  2. Exporta o teu perfil LinkedIn como PDF"
echo "     LinkedIn → Perfil → Mais → Guardar como PDF"
echo ""
echo "  3. Coloca o PDF em data/inputs/"
echo ""
echo "  4. Executa a análise:"
echo "     $ python src/cli.py analyze-perfil data/inputs/perfil.pdf"
echo ""
echo "📚 Documentação completa em docs/GUIA_USO.md"
echo ""
