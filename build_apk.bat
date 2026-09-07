@echo off
title Compilar APK do Agendador
echo Iniciando compilacao fora do Android Studio...
echo.

:: Executa o wrapper do gradle para construir a versao Release
call gradlew assembleRelease

echo.
if exist "app\build\outputs\apk\release\app-release.apk" (
    echo Copiando APK para a pasta principal...
    copy "app\build\outputs\apk\release\app-release.apk" "AgendadorPro.apk"
    echo Sucesso! O arquivo AgendadorPro.apk esta pronto na raiz do projeto.
) else (
    echo Erro ao encontrar o APK. Verifique se a compilacao falhou.
)
pause
