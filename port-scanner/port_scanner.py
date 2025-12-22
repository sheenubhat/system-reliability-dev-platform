
import socket
import argparse
import json
import os
import sys

LOG_DIR = "runtime-logs"
LOG_FILE = os.path.join(LOG_DIR, "system.log")

os.makedirs(LOG_DIR, exist_ok=True)
open(LOG_FILE, "a").close()

def log(message, level="INFO"):
    with open(LOG_FILE, "a") as f:
        f.write(f"{level} {message}\n")

OUTPUT_DIR = "port-scanner/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "scan_results.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def scan(host, ports):
    results = {}

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            rc = sock.connect_ex((host, port))

            status = "OPEN" if rc == 0 else "CLOSED"
            results[str(port)] = status

            print(f"Port {port}: {status}")

            if status == "OPEN":
                log(f"Port {port} open on {host}")
            else:
                log(f"Port {port} closed on {host}", level="WARN")

        except socket.gaierror:
            results[str(port)] = "INVALID_HOST"
            log(f"Invalid host {host}", level="ERROR")
            print(f"Port {port}: INVALID HOST")

        except Exception as e:
            results[str(port)] = f"ERROR: {e}"
            log(f"Error scanning port {port} on {host}: {e}", level="ERROR")
            print(f"Port {port}: ERROR")

        finally:
            try:
                sock.close()
            except Exception:
                pass

    return results

def write_json(host, results):
    if results is None:
        log("scan() returned None", level="ERROR")
        sys.exit(1)

    data = {
        "host": host,
        "results": results
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\nJSON output written to: {OUTPUT_FILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Port Scanner with Logging and JSON Output")
    parser.add_argument("host", help="Target host")
    parser.add_argument("--ports", required=True, help="Comma-separated ports")
    args = parser.parse_args()

    ports = [int(p.strip()) for p in args.ports.split(",")]

    log("Port scanner started")
    scan_results = scan(args.host, ports)
    write_json(args.host, scan_results)

