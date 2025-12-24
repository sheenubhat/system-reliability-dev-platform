
# coordinate ping, port scan, log analysis 

import json
import subprocess
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PORT_SCAN_OUTPUT = os.path.join(
    BASE_DIR, "port-scanner", "output", "scan_results.json"
)

SYSTEM_LOG = os.path.join(
    BASE_DIR, "runtime-logs", "system.log"
)

OUTPUT_DIR = os.path.join(BASE_DIR, "orchestrator", "output")
FINAL_OUTPUT = os.path.join(OUTPUT_DIR, "system_state.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_port_scan():
    with open(PORT_SCAN_OUTPUT) as f:
        return json.load(f)

def analyze_logs():
    alerts = []
    with open(SYSTEM_LOG) as f:
        for line in f:
            if "ERROR" in line or "WARN" in line:
                alerts.append(line.strip())
    return alerts

def decide_health(port_results, alerts):
    closed_ports = [
        p for p, status in port_results["results"].items()
        if status != "OPEN"
    ]

    if alerts and closed_ports:
        return "UNHEALTHY"
    if alerts or closed_ports:
        return "DEGRADED"
    return "HEALTHY"

def main():
    print("[ORCHESTRATOR] Evaluating system")

    port_data = load_port_scan()
    alerts = analyze_logs()
    health = decide_health(port_data, alerts)

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "health": health,
        "ports": port_data,
        "alerts": alerts
    }

    with open(FINAL_OUTPUT, "w") as f:
        json.dump(result, f, indent=2)

    print(f"[ORCHESTRATOR] System health: {health}")

    if health != "HEALTHY":
        sys.exit(1)

if __name__ == "__main__":
    main()
