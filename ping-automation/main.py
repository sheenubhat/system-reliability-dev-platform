
# simple host availability checker
from flask import Flask, jsonify, request
import subprocess
import json
import os
import platform


# Logging setup

LOG_DIR = "runtime-logs"
LOG_FILE = os.path.join(LOG_DIR, "system.log")

os.makedirs(LOG_DIR, exist_ok=True)
open(LOG_FILE, "a").close()

def log(message, level="INFO"):
    with open(LOG_FILE, "a") as f:
        f.write(f"{level} {message}\n")

app = Flask(__name__)
results = {}

OUTPUT_DIR = "ping-automation/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "results.json")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Ping logic (OS-safe)
def ping_host(host):
    try:
        system = platform.system().lower()

        if system == "windows":
            cmd = ["ping", "-n", "1", host]
        else:
            cmd = ["ping", "-c", "1", host]

        response = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )

        if response.returncode == 0:
            log(f"Ping success for {host}")
            return "reachable"
        else:
            log(f"Ping failed for {host}", level="ERROR")
            return "unreachable"

    except Exception as e:
        log(f"Ping error for {host}: {e}", level="ERROR")
        return f"error: {e}"

def write_results():
    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)

# API endpoints
@app.route("/ping", methods=["POST"])
def ping():
    data = request.get_json()
    targets = data.get("targets", [])

    log(f"/ping called for targets: {targets}")

    for host in targets:
        results[host] = ping_host(host)

    write_results()
    return jsonify(results), 200

@app.route("/status", methods=["GET"])
def status():
    return jsonify(results), 200

if __name__ == "__main__":
    log("Ping automation service started")
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