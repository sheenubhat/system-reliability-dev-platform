import subprocess
import time
import sys

print("[SYSTEM] Starting ping service")

ping_process = subprocess.Popen(
    ["python", "ping-automation/main.py"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

time.sleep(5)  # give Flask time to start

print("[SYSTEM] Triggering ping API")

try:
    subprocess.run(
        [
            "powershell",
            "-Command",
            "Invoke-RestMethod "
            "-Uri http://localhost:8080/ping "
            "-Method Post "
            "-ContentType 'application/json' "
            "-Body '{\"targets\":[\"8.8.8.8\",\"1.1.1.1\"]}'"
        ],
        check=True
    )
except subprocess.CalledProcessError:
    print("[ERROR] Ping API failed")

time.sleep(2)

print("[SYSTEM] Running port scan")
subprocess.run(
    [
        "python",
        "port-scanner/port_scanner.py",
        "127.0.0.1",
        "--ports",
        "22,80,443"
    ]
)

time.sleep(1)

print("[SYSTEM] Running orchestrator")
subprocess.run(
    [
        "python",
        "orchestrator/orchestrator.py"
    ]
)

print("[SYSTEM] Shutting down ping service")
ping_process.terminate()
