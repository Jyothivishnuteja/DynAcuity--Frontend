@echo off
echo ==========================================
echo DynAcuity Emergency Service Restarter
echo ==========================================

echo [1/4] Killing old processes...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM ssh.exe /T >nul 2>&1
taskkill /F /IM ngrok.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

echo [2/4] Starting Django Backend (Port 8000)...
start "Django" /min cmd /c "C:\Users\vishn\AppData\Local\Programs\Python\Python312\python.exe c:\Users\vishn\AndroidStudioProjects\dynacuity_backend\manage.py runserver 127.0.0.1:8000 --noreload > django_log.txt 2>&1"

echo [3/4] Starting Unified Proxy (Port 3000)...
start "Proxy" /min cmd /c "C:\Users\vishn\AppData\Local\Programs\Python\Python312\python.exe c:\Users\vishn\AndroidStudioProjects\DynAcuityWeb\serve_proxy.py > proxy_log.txt 2>&1"

echo [4/4] Starting SSH Tunnel (localhost.run)...
:tunnel_loop
echo Starting tunnel...
ssh -o StrictHostKeyChecking=no -R 80:127.0.0.1:8000 nokey@localhost.run
echo Tunnel dropped! Restarting in 5 seconds...
timeout /t 5
goto tunnel_loop

echo.
echo ==========================================
echo SERVICES STARTED! 
echo PLEASE WAIT 10 SECONDS FOR THE TUNNEL URL.
echo IF SIR IS CHECKING: COPY THE NEW HTTPS URL 
echo FROM THE TUNNEL WINDOW THAT JUST OPENED.
echo ==========================================
pause
