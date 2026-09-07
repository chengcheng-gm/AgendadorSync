@echo off
title Criar Executavel PC
echo Preparando ambiente Python...
pip install pyinstaller

echo.
echo Compilando aplicativo PC (isso pode demorar um pouco)...
:: --noconsole esconde a janela preta do terminal ao abrir o app
:: --onefile junta tudo num .exe so
pyinstaller --noconsole --onefile pc_agendador.py

echo.
if exist "dist\pc_agendador.exe" (
    echo Aplicativo compilado com sucesso!
    echo O arquivo executavel esta dentro da pasta 'dist'.
) else (
    echo Ocorreu um erro na compilacao.
)
pause
