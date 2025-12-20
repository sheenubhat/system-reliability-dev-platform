
# simple host availability checker

import subprocess
import argparse
from flask import Flask, jsonify 
import threading

app = Flask(__name__)
results = {}

def pingHost(host):
    try:
        output = subprocess.run(
            ["ping", "-c", "1", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
            
        )
        results[host]= "reachable" if output.returncode == 0 else "unreachable"
    except Exception:
        results[host] = "error"


@app.route("/status")
def status():
    return jsonify(results)

def start_api():
    app.run(host="0.0.0.0", port=8080)

#  main

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", nargs="+", required=True)
    args = parser.parse_args()


    for t in args.targets:
        pingHost(t)

    threading.Thread(target=start_api).start()
