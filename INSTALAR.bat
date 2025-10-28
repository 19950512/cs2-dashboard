@echo off
title CS2 Stats - Instalacao Automatica
color 0A

echo.
echo ========================================
echo    CS2 Stats Collector
echo    Instalacao Automatica para Amigos
echo ========================================
echo.

echo [INFO] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo [INFO] Baixe o Python em: https://python.org
    echo [IMPORTANTE] Marque "Add Python to PATH" durante a instalacao
    echo.
    pause
    exit /b 1
)
echo [OK] Python encontrado!

echo.
echo [INFO] Criando ambiente virtual...
python -m venv cs2_env
if errorlevel 1 (
    echo [ERRO] Erro ao criar ambiente virtual
    pause
    exit /b 1
)

echo [INFO] Ativando ambiente...
call cs2_env\Scripts\activate.bat

echo [INFO] Instalando dependencias...
pip install flask requests
if errorlevel 1 (
    echo [ERRO] Erro ao instalar dependencias
    pause
    exit /b 1
)

echo.
echo [INFO] Configurando CS2...
set "CS2_CFG=%PROGRAMFILES(X86)%\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg"
if not exist "%CS2_CFG%" (
    echo [AVISO] CS2 nao encontrado no local padrao!
    echo [INFO] Copie manualmente o arquivo gamestate_integration_main.cfg para:
    echo        [SUA_PASTA_CS2]\game\csgo\cfg\
    echo.
) else (
    copy /Y "gamestate_integration_main.cfg" "%CS2_CFG%\"
    if errorlevel 1 (
        echo [AVISO] Nao foi possivel copiar automaticamente
        echo [INFO] Copie manualmente o arquivo gamestate_integration_main.cfg para:
        echo        %CS2_CFG%\
    ) else (
        echo [OK] Arquivo copiado para CS2!
    )
)

echo.
echo ========================================
echo           INSTALACAO CONCLUIDA!
echo ========================================
echo.
echo Para usar:
echo    1. Execute: INICIAR.bat
echo    2. Abra o CS2
echo    3. Jogue algumas partidas
echo    4. Suas stats serao enviadas automaticamente!
echo.
echo Para ver stats do grupo: dashboard.html
echo.
pause