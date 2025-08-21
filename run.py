#!/usr/bin/env python3
"""
Script para executar o Sistema de Busca de Arquivos
"""
import os
import sys
from app import create_app

def main():
    """Função principal para executar a aplicação"""
    
    # Determinar ambiente
    env = os.environ.get('FLASK_ENV', 'development')
    
    print(f"🚀 Iniciando Sistema de Busca de Arquivos em modo: {env}")
    print("=" * 50)
    
    try:
        # Criar aplicação
        app = create_app(env)
        
        # Configurações
        host = app.config.get('HOST', '0.0.0.0')
        port = app.config.get('PORT', 5000)
        debug = app.config.get('DEBUG', True)
        
        print(f"📍 Servidor rodando em: http://{host}:{port}")
        print(f"🔧 Modo debug: {'Ativado' if debug else 'Desativado'}")
        print(f"📁 Pasta de uploads: {app.config.get('UPLOAD_FOLDER', 'uploads')}")
        print(f"📊 Arquivo de índice: {app.config.get('INDEX_FILE', 'search_index.json')}")
        print("=" * 50)
        print("💡 Dicas:")
        print("   - Use Ctrl+C para parar o servidor")
        print("   - Acesse http://localhost:5000 no navegador")
        print("   - Envie arquivos Word (.docx) e PDF para testar")
        print("=" * 50)
        
        # Executar aplicação
        app.run(host=host, port=port, debug=debug)
        
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
