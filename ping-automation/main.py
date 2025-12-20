
# simple host availability checker


# import argparse
from flask import Flask, jsonify, request 
import subprocess
import json
import os
# # import threading

app = Flask(__name__)
results = {}

OUTPUT_DIR = "ping-automation/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "results.json")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def ping_host(host):
    try:
        output = subprocess.run(
            ["ping",  host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            shell=True
            
        )
        return "reachable" if output.returncode == 0 else "unreachable"
    except Exception as e:
        return f"error: {e}"

def have_results():
    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)

@app.route("/ping", methods=["POST"])
def ping():
    data = request.json
    targets = data.get("targets", [])

    for host in targets:
        results[host] = ping_host(host)
    
    have_results()
    return jsonify(results), 200


@app.route("/status", methods=["GET"])
def status():
    return jsonify(results), 200

# def start_api():
#     app.run(host="0.0.0.0", port=8080)

#  main

if __name__ =="__main__":
    print("Starting Ping Automation Service.......")
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--targets", nargs="+", required=True)
    # args = parser.parse_args()




    # threading.Thread(target=start_api).start()
    app.run(host="127.0.0.1", port=8080)