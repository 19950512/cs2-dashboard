@echo off
title CS2 Stats - Coletando Dados
color 0B

echo.
echo ========================================
echo      CS2 Stats Collector
echo        Coletando suas stats...
echo ========================================
echo.

if not exist "cs2_env" (
    echo [ERRO] Ambiente nao encontrado!
    echo [INFO] Execute primeiro: INSTALAR.bat
    echo.
    pause
    exit /b 1
)

echo [INFO] Ativando ambiente...
call cs2_env\Scripts\activate.bat

echo [INFO] Iniciando coleta de dados...
echo.
echo DICAS:
echo    - Abra o CS2 e jogue normalmente
echo    - As stats serao enviadas automaticamente
echo    - Para parar: Ctrl+C
echo    - Status: http://127.0.0.1:3000/status
echo.
echo ========================================
echo.

python cs2_stats.py

echo.
echo Coleta finalizada!
pause