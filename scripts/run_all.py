import subprocess
import time

print("[SYSTEM] Triggering ping")
subprocess.run([
    "powershell",
    "-Command",
    "Invoke-RestMethod -Uri http://localhost:8080/ping "
    "-Method Post -ContentType 'application/json' "
    "-Body '{\"targets\":[\"8.8.8.8\",\"1.1.1.1\"]}'"
])

time.sleep(2)

print("[SYSTEM] Running port scan")
subprocess.run([
    "python",
    "port-scanner/port_scanner.py",
    "127.0.0.1",
    "--ports",
    "22,80,443"
])

time.sleep(1)

print("[SYSTEM] Running orchestrator")
subprocess.run([
    "python",
    "orchestrator/orchestrator.py"
])
