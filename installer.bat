@echo off
echo ========================================
echo Sistema de Busca de Arquivos - Instalador
echo ========================================
echo.

REM Verificar se já está instalado
if exist "%ProgramFiles%\SistemaBuscaArquivos" (
    echo Desinstalando versao anterior...
    rmdir /s /q "%ProgramFiles%\SistemaBuscaArquivos"
)

REM Criar diretório de instalação
echo Criando diretorio de instalacao...
mkdir "%ProgramFiles%\SistemaBuscaArquivos"

REM Copiar arquivos
echo Copiando arquivos...
copy "SistemaBuscaArquivos.exe" "%ProgramFiles%\SistemaBuscaArquivos\"

REM Criar atalho no menu iniciar
echo Criando atalho no menu iniciar...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Sistema de Busca de Arquivos.lnk'); $Shortcut.TargetPath = '%ProgramFiles%\SistemaBuscaArquivos\SistemaBuscaArquivos.exe'; $Shortcut.Save()"

REM Criar atalho na área de trabalho
echo Criando atalho na area de trabalho...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Sistema de Busca de Arquivos.lnk'); $Shortcut.TargetPath = '%ProgramFiles%\SistemaBuscaArquivos\SistemaBuscaArquivos.exe'; $Shortcut.Save()"

echo.
echo ========================================
echo Instalacao concluida com sucesso!
echo ========================================
echo.
echo O programa foi instalado em: %ProgramFiles%\SistemaBuscaArquivos
echo Atalhos criados no menu iniciar e area de trabalho
echo.
pause
