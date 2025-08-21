@echo off
echo ========================================
echo Sistema de Busca de Arquivos - Desinstalador
echo ========================================
echo.

echo Tem certeza que deseja desinstalar? (S/N)
set /p confirm=

if /i "%confirm%"=="S" (
    echo Desinstalando...
    
    REM Remover atalhos
    if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Sistema de Busca de Arquivos.lnk" (
        del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Sistema de Busca de Arquivos.lnk"
    )
    
    if exist "%USERPROFILE%\Desktop\Sistema de Busca de Arquivos.lnk" (
        del "%USERPROFILE%\Desktop\Sistema de Busca de Arquivos.lnk"
    )
    
    REM Remover diretório de instalação
    if exist "%ProgramFiles%\SistemaBuscaArquivos" (
        rmdir /s /q "%ProgramFiles%\SistemaBuscaArquivos"
    )
    
    echo Desinstalacao concluida!
) else (
    echo Desinstalacao cancelada.
)

pause
