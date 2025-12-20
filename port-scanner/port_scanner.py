
import socket
import argparse
import json
import os
import sys

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
            results[str(port)] = status  # stringify for JSON
            # if result == 0:
        #     print(f"Port {port}: OPEN")
        # else:
        #     print(f"Port {port}: CLOSED")
            print(f"Port {port}: {status}")

        except socket.gaierror:
            results[str(port)] = "INVALID_HOST"
            print(f"Port {port}: INVALID HOST")

        except Exception as e:
            results[str(port)] = f"ERROR: {e}"
            print(f"Port {port}: ERROR")

        finally:
            try:
                sock.close()
            except Exception:
                pass

    return results   

def write_json(host, results):
    if results is None:
        print("ERROR: scan() returned None")
        sys.exit(1)

    data = {
        "host": host,
        "results": results
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\nJSON output written to: {OUTPUT_FILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Port Scanner with JSON Output")
    parser.add_argument("host", help="Target host")
    parser.add_argument("--ports", required=True, help="Comma-separated ports")
    args = parser.parse_args()

    ports = [int(p.strip()) for p in args.ports.split(",")]

    scan_results = scan(args.host, ports)
    write_json(args.host, scan_results)


        