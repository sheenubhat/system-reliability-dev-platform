
# simple host availability checker
from flask import Flask, jsonify, request
import subprocess
import json
import os
import platform

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_DIR = os.path.join(BASE_DIR, "runtime-logs")
LOG_FILE = os.path.join(LOG_DIR, "system.log")

OUTPUT_DIR = os.path.join(BASE_DIR, "ping-automation", "output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "results.json")

LOG_ANALYZER = os.path.join(BASE_DIR, "log-analyzer", "log_analyzer.py")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

open(LOG_FILE, "a").close()


def log(message, level="INFO"):
    with open(LOG_FILE, "a") as f:
        f.write(f"{level} {message}\n")


def ping_host(host):
    try:
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", "1", host]
        else:
            cmd = ["ping", "-c", "1", host]

        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5
        )

        return "reachable" if result.returncode == 0 else "unreachable"

    except subprocess.TimeoutExpired:
        return "timeout"
    except Exception as e:
        log(f"Ping failed for {host}: {e}", "ERROR")
        return "error"


def run_log_analyzer():
    try:
        subprocess.run(
            ["python", LOG_ANALYZER, LOG_FILE],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        log(f"Log analyzer failed: {e}", "ERROR")

# ------API endpoints ----------------
'''
    Automatically pipe logs into log-analyzer. Return HTTP 500 if ANY host fails
    If all hosts reachable → HTTP 200
    If any host unreachable/error → HTTP 500
    Response body still returns per-host results
    '''
@app.route("/ping", methods=["POST"])
def ping():
    data = request.get_json()
    targets = data.get("targets", [])

    results = {}
    failed = False

    log(f"/ping called for targets: {targets}")

    for host in targets:
        status = ping_host(host)
        results[host] = status

        if status != "reachable":
            log(f"Ping failed for {host}", "ERROR")
            failed = True
        else:
            log(f"Ping success for {host}")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)

    run_log_analyzer()

    if failed:
        return jsonify(results), 500

    return jsonify(results), 200


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"service": "running"}), 200


if __name__ == "__main__":
    print("Starting Ping Automation Service...")
    app.run(host="127.0.0.1", port=8080)




# import argparse
# from flask import Flask, jsonify, request 
# import subprocess
# import json
# import os
# # # import threading
# LOG_DIR = "runtime-logs"
# LOG_FILE = os.path.join(LOG_DIR, "system.log")

# os.makedirs(LOG_DIR, exist_ok=True)
# open(LOG_FILE, "a").close()

# def log(message, level="INFO"):
#     with open(LOG_FILE, "a") as f:
#         f.write(f"{level} {message}\n")


# app = Flask(__name__)
# results = {}

# OUTPUT_DIR = "ping-automation/output"
# OUTPUT_FILE = os.path.join(OUTPUT_DIR, "results.json")
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# def ping_host(host):
#     try:
#         output = subprocess.run(
#             ["ping",  host],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             timeout=5,
#             shell=True
            
#         )
#         return "reachable" if output.returncode == 0 else "unreachable"
#     except Exception as e:
#         return f"error: {e}"

# def have_results():
#     with open(OUTPUT_FILE, "w") as f:
#         json.dump(results, f, indent=2)

# @app.route("/ping", methods=["POST"])
# def ping():
#     data = request.json
#     targets = data.get("targets", [])

#     for host in targets:
#         results[host] = ping_host(host)
    
#     have_results()
#     return jsonify(results), 200


# @app.route("/status", methods=["GET"])
# def status():
#     return jsonify(results), 200

# # def start_api():
# #     app.run(host="0.0.0.0", port=8080)

# #  main

# if __name__ =="__main__":
#     print("Starting Ping Automation Service.......")
#     # parser = argparse.ArgumentParser()
#     # parser.add_argument("--targets", nargs="+", required=True)
#     # args = parser.parse_args()




#     # threading.Thread(target=start_api).start()
#     app.run(host="127.0.0.1", port=8080)