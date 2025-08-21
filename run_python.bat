@echo off
echo ========================================
echo Sistema de Busca de Arquivos - Python
echo ========================================
echo.

REM Definir caminhos do Python
set PYTHON_PATH=C:\Users\Administrador\AppData\Local\Programs\Python\Python313
set PYTHON=%PYTHON_PATH%\python.exe
set PIP=%PYTHON_PATH%\Scripts\pip.exe

echo Python encontrado em: %PYTHON_PATH%
echo.

REM Verificar versão do Python
echo Verificando versao do Python...
%PYTHON% --version
echo.

REM Verificar versão do pip
echo Verificando versao do pip...
%PIP% --version
echo.

REM Instalar dependências
echo Instalando dependencias...
%PIP% install -r requirements.txt
echo.

REM Executar aplicação
echo Executando aplicacao...
%PYTHON% app.py

pause
