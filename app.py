"""
Cloud Honeypot Attack Monitoring System
=======================================
A safe, lightweight, local educational honeypot built with Python Flask.
Designed to capture, count, and analyze unauthorized authentication attempts.

SAFETY & PRIVACY GUARANTEE:
- Passwords entered into this decoy system are NEVER stored, saved, or logged.
- The service binds strictly to 127.0.0.1 (localhost) for safe offline testing.
"""

from datetime import datetime
import json
import os
import sys

# Configure UTF-8 safe stdout for Windows console compatibility
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# In-memory storage for honeypot telemetry
# Each log entry contains only metadata: timestamp, ip, username, user_agent
honeypot_logs = []
LOG_FILE = "honeypot_events.json"


def load_logs():
    """Load previously recorded events from local JSON file if available."""
    global honeypot_logs
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                honeypot_logs = json.load(f)
        except Exception as e:
            print(f"[!] Warning: Could not load existing logs: {e}")
            honeypot_logs = []


def save_logs():
    """Save event metadata (without passwords) to local JSON file."""
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(honeypot_logs, f, indent=2)
    except Exception as e:
        print(f"[!] Warning: Could not save logs: {e}")


# Initialize existing logs on startup
load_logs()


@app.route("/")
def home():
    """
    Home page:
    Provides an introduction to the honeypot system, current attempt counters,
    and navigation to the decoy login and SOC monitoring dashboard.
    """
    total_attempts = len(honeypot_logs)
    return render_template("index.html", total_attempts=total_attempts)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Decoy Login Endpoint (Honeypot Trap):
    - GET: Displays a realistic fake cloud console login page.
    - POST: Intercepts unauthorized authentication attempts, logs telemetry,
      increments failed attempt count, and returns an error message.

    SAFETY NOTE: The password is NEVER logged, stored, or processed.
    """
    if request.method == "POST":
        # 1. Capture safe metadata
        username = request.form.get("username", "").strip() or "(empty)"
        
        # 2. PRIVACY & SAFETY: Discard password immediately
        # We explicitly do not log, retain, or store passwords anywhere.
        _ = request.form.get("password")  # Consumed and discarded
        
        # 3. Determine client IP and User Agent
        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        if client_ip and "," in client_ip:
            client_ip = client_ip.split(",")[0].strip()
        user_agent = request.headers.get("User-Agent", "Unknown")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 4. Record event telemetry
        event_record = {
            "id": len(honeypot_logs) + 1,
            "timestamp": timestamp,
            "username": username,
            "ip": client_ip,
            "user_agent": user_agent,
            "status": "Failed Login (Honeypot Triggered)",
            "password_stored": False
        }
        honeypot_logs.append(event_record)
        save_logs()

        print(f"[HONEYPOT TRIGGERED] Time: {timestamp} | Target User: '{username}' | IP: {client_ip} | Password: [DISCARDED]")

        error_message = (
            "Access Denied: Invalid credentials. "
            "This unauthorized attempt has been recorded by the honeypot monitor."
        )
        return render_template("login.html", error_message=error_message)

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    """
    SOC Monitoring Dashboard:
    Visualizes total attempts, unique targets, source IPs, and event logs.
    """
    total_attempts = len(honeypot_logs)
    unique_usernames = len(set(log["username"] for log in honeypot_logs))
    unique_ips = len(set(log["ip"] for log in honeypot_logs))

    # Show newest entries first
    reversed_logs = list(reversed(honeypot_logs))

    return render_template(
        "dashboard.html",
        total_attempts=total_attempts,
        unique_usernames_count=unique_usernames,
        unique_ips_count=unique_ips,
        logs=reversed_logs
    )


@app.route("/api/stats")
def api_stats():
    """API endpoint to query current attack telemetry in JSON format."""
    total_attempts = len(honeypot_logs)
    unique_usernames = list(set(log["username"] for log in honeypot_logs))
    unique_ips = list(set(log["ip"] for log in honeypot_logs))

    return jsonify({
        "status": "active",
        "mode": "local_safe_honeypot",
        "total_failed_attempts": total_attempts,
        "unique_usernames_count": len(unique_usernames),
        "unique_ips_count": len(unique_ips),
        "passwords_stored": False,
        "recent_events": honeypot_logs[-10:]
    })


@app.route("/reset", methods=["POST"])
def reset_logs():
    """Reset honeypot logs and counters for testing demonstrations."""
    global honeypot_logs
    honeypot_logs = []
    if os.path.exists(LOG_FILE):
        try:
            os.remove(LOG_FILE)
        except Exception as e:
            print(f"[!] Could not delete log file: {e}")
    print("[HONEYPOT] Logs and counters have been reset.")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("[*] Cloud Honeypot Attack Monitoring System")
    print("=" * 60)
    print(" [+] Listening on:    http://127.0.0.1:5000")
    print(" [+] Decoy Login:     http://127.0.0.1:5000/login")
    print(" [+] SOC Dashboard:   http://127.0.0.1:5000/dashboard")
    print(" [+] Safety Status:   Passwords are NEVER stored or logged")
    print(" [+] Mode:            Completely local & safe")
    print("=" * 60 + "\n")

    # Run on localhost only (127.0.0.1) for complete local safety
    app.run(host="127.0.0.1", port=5000, debug=True)
