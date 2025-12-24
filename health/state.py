# health check

def classify(ping_ok, open_ports, alerts):
    if not ping_ok:
        return "UNHEALTHY"
    
    if alerts or open_ports < 1:
        return "DEGRADED"
    
    return "HEALTHY"