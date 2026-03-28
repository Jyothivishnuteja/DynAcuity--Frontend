@echo off
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM ngrok.exe /T >nul 2>&1
taskkill /F /IM ssh.exe /T >nul 2>&1

echo Starting Django Backend...
start "Django" /min cmd /c "C:\Users\vishn\AppData\Local\Programs\Python\Python312\python.exe c:\Users\vishn\AndroidStudioProjects\dynacuity_backend\manage.py runserver 0.0.0.0:8000 --noreload > c:\Users\vishn\AndroidStudioProjects\dynacuity_backend\django_stdout.log 2>&1"

echo Starting Unified Proxy...
start "Proxy" /min cmd /c "C:\Users\vishn\AppData\Local\Programs\Python\Python312\python.exe c:\Users\vishn\AndroidStudioProjects\DynAcuityWeb\serve_proxy.py > c:\Users\vishn\AndroidStudioProjects\DynAcuityWeb\proxy_stdout.log 2>&1"

echo Starting SSH Tunnel (localhost.run)...
start "Tunnel" /min cmd /c "ssh -o StrictHostKeyChecking=no -R 80:localhost:8000 nokey@localhost.run > c:\Users\vishn\AndroidStudioProjects\DynAcuityWeb\ssh_tunnel.log 2>&1"

echo Services started.
ping 127.0.0.1 -n 6 > nul
