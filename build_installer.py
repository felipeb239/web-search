"""
Script para gerar o instalador executável do Sistema de Busca
"""
import os
import subprocess
import sys

def install_pyinstaller():
    """Instala o PyInstaller se não estiver instalado"""
    try:
        import PyInstaller
        print("✅ PyInstaller já está instalado")
    except ImportError:
        print("📦 Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller instalado com sucesso!")

def build_executable():
    """Gera o executável"""
    print("🔨 Gerando executável...")
    
    # Comando PyInstaller
    cmd = [
        "C:\\Users\\Administrador\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\pyinstaller.exe",
        "--onefile",                    # Arquivo único
        "--windowed",                   # Sem console (aplicação desktop)
        "--name=SistemaBuscaArquivos",  # Nome do executável
        "--icon=icon.ico",              # Ícone (se existir)
        "--add-data=desktop_config.json;.",  # Incluir arquivo de configuração
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=docx",
        "--hidden-import=PyPDF2",
        "--hidden-import=ftplib",
        "desktop_app.py"
    ]
    
    # Remover parâmetros que podem não existir
    if not os.path.exists("icon.ico"):
        cmd.remove("--icon=icon.ico")
    
    try:
        subprocess.check_call(cmd)
        print("✅ Executável gerado com sucesso!")
        print("📁 Arquivo criado em: dist/SistemaBuscaArquivos.exe")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao gerar executável: {e}")
        return False
    
    return True

def create_installer_script():
    """Cria script de instalação"""
    print("📝 Criando script de instalação...")
    
    installer_content = '''@echo off
echo ========================================
echo Sistema de Busca de Arquivos - Instalador
echo ========================================
echo.

REM Verificar se já está instalado
if exist "%ProgramFiles%\\SistemaBuscaArquivos" (
    echo Desinstalando versao anterior...
    rmdir /s /q "%ProgramFiles%\\SistemaBuscaArquivos"
)

REM Criar diretório de instalação
echo Criando diretorio de instalacao...
mkdir "%ProgramFiles%\\SistemaBuscaArquivos"

REM Copiar arquivos
echo Copiando arquivos...
copy "SistemaBuscaArquivos.exe" "%ProgramFiles%\\SistemaBuscaArquivos\\"

REM Criar atalho no menu iniciar
echo Criando atalho no menu iniciar...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Sistema de Busca de Arquivos.lnk'); $Shortcut.TargetPath = '%ProgramFiles%\\SistemaBuscaArquivos\\SistemaBuscaArquivos.exe'; $Shortcut.Save()"

REM Criar atalho na área de trabalho
echo Criando atalho na area de trabalho...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Sistema de Busca de Arquivos.lnk'); $Shortcut.TargetPath = '%ProgramFiles%\\SistemaBuscaArquivos\\SistemaBuscaArquivos.exe'; $Shortcut.Save()"

echo.
echo ========================================
echo Instalacao concluida com sucesso!
echo ========================================
echo.
echo O programa foi instalado em: %ProgramFiles%\\SistemaBuscaArquivos
echo Atalhos criados no menu iniciar e area de trabalho
echo.
pause
'''
    
    with open("installer.bat", "w", encoding="utf-8") as f:
        f.write(installer_content)
    
    print("✅ Script de instalação criado: installer.bat")

def create_uninstaller():
    """Cria desinstalador"""
    print("🗑️ Criando desinstalador...")
    
    uninstaller_content = '''@echo off
echo ========================================
echo Sistema de Busca de Arquivos - Desinstalador
echo ========================================
echo.

echo Tem certeza que deseja desinstalar? (S/N)
set /p confirm=

if /i "%confirm%"=="S" (
    echo Desinstalando...
    
    REM Remover atalhos
    if exist "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Sistema de Busca de Arquivos.lnk" (
        del "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Sistema de Busca de Arquivos.lnk"
    )
    
    if exist "%USERPROFILE%\\Desktop\\Sistema de Busca de Arquivos.lnk" (
        del "%USERPROFILE%\\Desktop\\Sistema de Busca de Arquivos.lnk"
    )
    
    REM Remover diretório de instalação
    if exist "%ProgramFiles%\\SistemaBuscaArquivos" (
        rmdir /s /q "%ProgramFiles%\\SistemaBuscaArquivos"
    )
    
    echo Desinstalacao concluida!
) else (
    echo Desinstalacao cancelada.
)

pause
'''
    
    with open("uninstaller.bat", "w", encoding="utf-8") as f:
        f.write(uninstaller_content)
    
    print("✅ Desinstalador criado: uninstaller.bat")

def create_readme():
    """Cria arquivo README para o usuário final"""
    print("📖 Criando documentação...")
    
    readme_content = '''# Sistema de Busca de Arquivos - Desktop

## Descrição
Sistema profissional para busca e indexação de arquivos Word (.docx) e PDF em servidores de arquivos.

## Recursos
- ✅ Conexão com servidores locais, FTP, SMB e WebDAV
- ✅ Indexação automática de documentos
- ✅ Busca por nome e conteúdo dos arquivos
- ✅ Interface desktop profissional
- ✅ Sistema de relevância inteligente
- ✅ Estatísticas de indexação

## Tipos de Servidor Suportados

### 1. Servidor Local
- Caminho para pasta local na máquina
- Exemplo: C:\\Documentos\\Empresa

### 2. Servidor FTP
- Host/IP do servidor FTP
- Porta (padrão: 21)
- Usuário e senha
- Caminho no servidor

### 3. Servidor SMB (Windows/Network)
- Host/IP do servidor
- Usuário e senha de domínio
- Caminho compartilhado

### 4. Servidor WebDAV
- URL do servidor WebDAV
- Usuário e senha
- Caminho no servidor

## Como Usar

### Primeira Configuração
1. Abra o programa
2. Configure o tipo de servidor
3. Preencha as informações de conexão
4. Clique em "Conectar" para testar
5. Clique em "Salvar Config" para salvar

### Indexação
1. Após conectar, clique em "Indexar Arquivos"
2. Aguarde a indexação concluir
3. Verifique as estatísticas

### Busca
1. Digite o termo de busca na barra
2. Pressione Enter ou clique em "Buscar"
3. Visualize os resultados ordenados por relevância

## Suporte Técnico
Para suporte técnico, entre em contato com nossa equipe.

## Licença
Este software é licenciado para uso comercial.
'''
    
    with open("README_Usuario.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ Documentação criada: README_Usuario.txt")

def main():
    print("🚀 Iniciando processo de criação do instalador...")
    print()
    
    # 1. Instalar PyInstaller
    install_pyinstaller()
    print()
    
    # 2. Gerar executável
    if build_executable():
        print()
        
        # 3. Criar script de instalação
        create_installer_script()
        print()
        
        # 4. Criar desinstalador
        create_uninstaller()
        print()
        
        # 5. Criar documentação
        create_readme()
        print()
        
        print("🎉 Processo concluído com sucesso!")
        print()
        print("📁 Arquivos gerados:")
        print("  - dist/SistemaBuscaArquivos.exe (executável)")
        print("  - installer.bat (instalador)")
        print("  - uninstaller.bat (desinstalador)")
        print("  - README_Usuario.txt (documentação)")
        print()
        print("💡 Para distribuir:")
        print("  1. Compacte todos os arquivos em um ZIP")
        print("  2. Envie para seus clientes")
        print("  3. Eles executam installer.bat para instalar")
        
    else:
        print("❌ Falha na criação do executável")

if __name__ == "__main__":
    main()
