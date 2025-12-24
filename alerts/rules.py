# alert engine

def generate_alerts(logs):
    alerts = []

    for line in logs:
        if "ERROR" in line:
            alerts.append({
                "severity": "CRITICAL",
                "message": line
            })

        elif "WARN" in line:
            alerts.append({
                "severity": "WARNING",
                "message": line
            })

    
    return alerts