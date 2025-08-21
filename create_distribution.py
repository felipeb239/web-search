"""
Script para criar pacote de distribuição do Sistema de Busca de Arquivos
"""
import zipfile
import os
import shutil
from datetime import datetime

def create_distribution_package():
    """Cria o pacote de distribuição completo"""
    
    # Nome do arquivo ZIP
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"SistemaBuscaArquivos_v1.0_{timestamp}.zip"
    
    print(f"📦 Criando pacote de distribuição: {zip_filename}")
    print()
    
    # Arquivos necessários para distribuição
    files_to_include = [
        ("dist/SistemaBuscaArquivos.exe", "SistemaBuscaArquivos.exe"),
        ("installer.bat", "installer.bat"),
        ("uninstaller.bat", "uninstaller.bat"),
        ("README_Usuario.txt", "README_Usuario.txt")
    ]
    
    # Criar o ZIP
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for source_file, zip_path in files_to_include:
            if os.path.exists(source_file):
                zipf.write(source_file, zip_path)
                file_size = os.path.getsize(source_file)
                print(f"✅ Adicionado: {zip_path} ({file_size:,} bytes)")
            else:
                print(f"❌ Arquivo não encontrado: {source_file}")
    
    # Verificar tamanho do ZIP
    if os.path.exists(zip_filename):
        zip_size = os.path.getsize(zip_filename)
        print()
        print(f"🎉 Pacote criado com sucesso!")
        print(f"📁 Arquivo: {zip_filename}")
        print(f"📊 Tamanho: {zip_size:,} bytes ({zip_size / (1024*1024):.1f} MB)")
        print()
        print("📋 Conteúdo do pacote:")
        print("  - SistemaBuscaArquivos.exe (programa principal)")
        print("  - installer.bat (instalador)")
        print("  - uninstaller.bat (desinstalador)")
        print("  - README_Usuario.txt (manual)")
        print()
        print("💡 Para distribuir:")
        print(f"  1. Envie o arquivo {zip_filename} para seus clientes")
        print("  2. Cliente extrai o ZIP")
        print("  3. Cliente executa installer.bat como administrador")
        print("  4. Programa instalado e pronto para usar!")
        
        return zip_filename
    else:
        print("❌ Erro ao criar o pacote")
        return None

def create_developer_package():
    """Cria pacote completo para desenvolvedor"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"SistemaBuscaArquivos_Developer_{timestamp}.zip"
    
    print(f"🔧 Criando pacote para desenvolvedor: {zip_filename}")
    print()
    
    # Arquivos para desenvolvedor
    developer_files = [
        # Código fonte
        "desktop_app.py",
        "app.py",
        "routes.py",
        "config.py",
        "file_processor.py",
        "run.py",
        "build_installer.py",
        "create_distribution.py",
        
        # Configurações
        "requirements.txt",
        "desktop_config.json",
        ".gitignore",
        
        # Templates e static
        "templates/index.html",
        "static/css/style.css",
        "static/js/app.js",
        
        # Documentação
        "README.md",
        "README_Usuario.txt",
        
        # Scripts
        "run_python.bat",
        "installer.bat",
        "uninstaller.bat",
        
        # Executável
        "dist/SistemaBuscaArquivos.exe"
    ]
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in developer_files:
            if os.path.exists(file_path):
                zipf.write(file_path, file_path)
                file_size = os.path.getsize(file_path)
                print(f"✅ {file_path} ({file_size:,} bytes)")
            else:
                print(f"⚠️  Não encontrado: {file_path}")
    
    if os.path.exists(zip_filename):
        zip_size = os.path.getsize(zip_filename)
        print()
        print(f"🎉 Pacote desenvolvedor criado!")
        print(f"📁 Arquivo: {zip_filename}")
        print(f"📊 Tamanho: {zip_size:,} bytes ({zip_size / (1024*1024):.1f} MB)")
        
        return zip_filename
    
    return None

def main():
    print("🚀 Criador de Pacotes - Sistema de Busca de Arquivos")
    print("=" * 60)
    print()
    
    # 1. Criar pacote de distribuição (para clientes)
    dist_package = create_distribution_package()
    print()
    
    # 2. Criar pacote para desenvolvedor (código completo)
    dev_package = create_developer_package()
    print()
    
    print("📦 Resumo dos pacotes criados:")
    if dist_package:
        print(f"  🎯 Cliente: {dist_package}")
    if dev_package:
        print(f"  🔧 Desenvolvedor: {dev_package}")
    
    print()
    print("✨ Processo concluído com sucesso!")

if __name__ == "__main__":
    main()
