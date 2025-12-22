
import sys
import json
import os

OUTPUT_DIR = "log-analyzer/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "analysis.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def analyze_log(file_path):
    summary = {"INFO": 0, "WARN": 0, "ERROR": 0}
    events = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()

            if line.startswith("INFO"):
                summary["INFO"] += 1

            elif line.startswith("WARN"):
                summary["WARN"] += 1
                message = line.replace("WARN", "").strip().lower()
                events.append({"level": "WARN", "message": message})
                print(f"WARN {message}")

            elif line.startswith("ERROR"):
                summary["ERROR"] += 1
                message = line.replace("ERROR", "").strip().lower()
                events.append({"level": "ERROR", "message": message})
                print(f"ERROR {message}")

    return summary, events
def write_json(file_name, summary, events):
    data = {
        "file": file_name,
        "summary": summary,
        "events": events
    }
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\nJSON report written to {OUTPUT_FILE}")

if __name__ =="__main__":
    if len(sys.argv) != 2:
        print("Usage: python log_analyzer.py <logfile>")
        sys.exit(1)
    log_file = sys.argv[1]

    summary, events = analyze_log(log_file)
    write_json(log_file, summary, events)
