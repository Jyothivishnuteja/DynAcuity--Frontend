import subprocess
import time
import sys
import os

def run_services():
    print("=== DynAcuity Robust Service Runner ===")
    
    # 1. Kill old processes
    print("Cleaning up old processes...")
    subprocess.run("taskkill /F /IM python.exe /T", shell=True, capture_output=True)
    subprocess.run("taskkill /F /IM ssh.exe /T", shell=True, capture_output=True)
    
    # 2. Start Django
    print("Starting Django Backend (Port 8000)...")
    django_cmd = [
        sys.executable,
        r"c:\Users\vishn\AndroidStudioProjects\dynacuity_backend\manage.py",
        "runserver", "127.0.0.1:8000", "--noreload"
    ]
    django_proc = subprocess.Popen(django_cmd, stdout=open("django_stdout.log", "w"), stderr=subprocess.STDOUT)
    
    # 3. Start Proxy
    print("Starting Unified Proxy (Port 3000)...")
    proxy_cmd = [
        sys.executable,
        r"c:\Users\vishn\AndroidStudioProjects\DynAcuityWeb\serve_proxy.py"
    ]
    proxy_proc = subprocess.Popen(proxy_cmd, stdout=open("proxy_stdout.log", "w"), stderr=subprocess.STDOUT)
    
    time.sleep(5)
    
    # 4. Start Tunnel
    print("Starting Tunnel (localhost.run)...")
    # We point the tunnel to the PROXY (port 3000) so it serves both static and API
    tunnel_cmd = "ssh -o StrictHostKeyChecking=no -R 80:127.0.0.1:3000 nokey@localhost.run"
    
    # Run tunnel and capture output to get the URL
    with open("tunnel_output.log", "w") as log_file:
        tunnel_proc = subprocess.Popen(tunnel_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # We need to wait a bit for the URL to appear in the output
        print("Waiting for tunnel URL...")
        for line in iter(tunnel_proc.stdout.readline, ""):
            print(line.strip())
            log_file.write(line)
            if ".lhr.life" in line or ".localhost.run" in line:
                # Found the URL, save it
                with open("current_url.txt", "w") as f:
                    f.write(line.strip())
                print(f"\nFOUND URL: {line.strip()}")
                break
    
    print("\n" + "="*40)
    print("SERVICES ARE RUNNING!")
    print("Look at the NEW terminal window for your website link.")
    print("Keep THIS window open to keep the servers alive.")
    print("="*40)
    
    try:
        while True:
            if django_proc.poll() is not None:
                print("WARNING: Django died! Restarting...")
                django_proc = subprocess.Popen(django_cmd, stdout=open("django_stdout.log", "a"), stderr=subprocess.STDOUT)
            if proxy_proc.poll() is not None:
                print("WARNING: Proxy died! Restarting...")
                proxy_proc = subprocess.Popen(proxy_cmd, stdout=open("proxy_stdout.log", "a"), stderr=subprocess.STDOUT)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nStopping services...")
        django_proc.terminate()
        proxy_proc.terminate()

if __name__ == "__main__":
    run_services()
