#!/usr/bin/env python3
"""NEXUS Replit Worker - always online"""
from flask import Flask, request, jsonify
import requests as req
import threading
import time
import os

app = Flask(__name__)
VPS = "http://176.123.169.38:5000"
TASKS = []

def scanner(target):
    base = f"https://{target}" if not target.startswith("http") else target
    findings = []

    try:
        r = req.get(base, timeout=10, verify=False)
        h = r.headers
        if "X-Frame-Options" not in h: findings.append({"sev": "MEDIUM", "v": "Clickjacking"})
        if "Content-Security-Policy" not in h: findings.append({"sev": "LOW", "v": "No CSP"})
    except Exception as e:
        return {"error": str(e)}

    for p in ["/.env", "/.git/HEAD", "/api", "/admin"]:
        try:
            r2 = req.get(f"{base}{p}", timeout=5, verify=False, allow_redirects=False)
            if r2.status_code == 200:
                findings.append({"sev": "HIGH", "path": p})
        except:
            pass

    return {"target": target, "findings": findings, "worker": "replit"}

@app.route("/")
def home():
    return jsonify({"status": "NEXUS Replit Worker", "tasks": len(TASKS)})

@app.route("/scan/<target>")
def scan(target):
    result = scanner(target)
    req.post(f"{VPS}/catch/replit", json=result, timeout=10)
    return jsonify(result)

@app.route("/task", methods=["POST"])
def add_task():
    data = request.json
    TASKS.append(data.get("target"))
    return jsonify({"queued": data.get("target")})

def worker_loop():
    while True:
        if TASKS:
            target = TASKS.pop(0)
            result = scanner(target)
            req.post(f"{VPS}/catch/replit", json=result, timeout=10)
        time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=worker_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)
