@echo off
title Servidor Agendador Pro
echo Iniciando servidor web local na porta 8000...
start "Servidor Python" cmd /k "python -m http.server 8000"

echo Aguardando o servidor iniciar...
timeout /t 2 /nobreak > nul

echo Iniciando tunel do Cloudflare...
start "Cloudflare Tunnel" cmd /k "cloudflared tunnel --url http://localhost:8000"
