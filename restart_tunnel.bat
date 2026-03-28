@echo off
taskkill /F /IM ssh.exe /T >nul 2>&1
start /min ssh -o StrictHostKeyChecking=no -R 80:127.0.0.1:3000 nokey@localhost.run ^> ssh_tunnel.log 2^>^&1
