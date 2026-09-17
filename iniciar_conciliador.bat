@echo off
setlocal

REM =============================================================
REM  Conciliador Bancario - inicializador para Windows
REM
REM  Primeira execucao : cria o ambiente virtual e instala as
REM                       dependencias (requirements.txt).
REM  Proximas execucoes : apenas ativa o ambiente ja existente
REM                       e abre o app no navegador.
REM =============================================================

cd /d "%~dp0"

set VENV_DIR=venv

REM --- Detecta o comando de Python disponivel (python ou o launcher py) ---
set PY_CMD=

where python >nul 2>nul
if %errorlevel%==0 (
    set PY_CMD=python
) else (
    where py >nul 2>nul
    if %errorlevel%==0 (
        set PY_CMD=py -3
    )
)

if "%PY_CMD%"=="" (
    echo.
    echo [ERRO] Python nao foi encontrado neste computador.
    echo.
    echo Instale o Python em https://www.python.org/downloads/
    echo Durante a instalacao, marque a opcao "Add python.exe to PATH"
    echo antes de clicar em Install. Depois, execute este arquivo novamente.
    echo.
    pause
    exit /b 1
)

if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo ============================================
    echo  Primeira execucao: preparando o ambiente...
    echo  Isso pode levar alguns minutos.
    echo ============================================
    %PY_CMD% -m venv "%VENV_DIR%"

    if not exist "%VENV_DIR%\Scripts\activate.bat" (
        echo.
        echo [ERRO] Nao foi possivel criar o ambiente virtual com o comando: %PY_CMD%
        echo Tente reinstalar o Python marcando "Add python.exe to PATH".
        pause
        exit /b 1
    )

    call "%VENV_DIR%\Scripts\activate.bat"
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call "%VENV_DIR%\Scripts\activate.bat"
)

echo.
echo Iniciando o Conciliador Bancario...
echo O app vai abrir automaticamente no seu navegador.
echo Para encerrar, feche esta janela ou pressione CTRL+C.
echo.

streamlit run app.py

endlocal
