# Cloud Honeypot Attack Monitoring System

A safe, lightweight, local educational honeypot built with Python Flask to monitor and analyze simulated brute-force and credential probe attempts.

---

## 🔒 Safety & Privacy Principles

- **Zero-Password Storage**: Passwords submitted to the decoy login page are intercepted in memory and **immediately discarded**. They are never saved to disk, logged in terminal output, or stored in database tables.
- **Strictly Localhost**: The application binds by default to `127.0.0.1:5000` to prevent exposure to external networks.
- **Educational Context**: Designed for cybersecurity students, researchers, and developers learning honeypot architectures and SOC telemetry.

---

## 🚀 Quick Start

### 1. Run the Application
```bash
python app.py
```

### 2. Access the Web Interfaces
Open your browser and navigate to:
- **Home Page**: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- **Decoy Login Page**: [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)
- **SOC Monitoring Dashboard**: [http://127.0.0.1:5000/dashboard](http://127.0.0.1:5000/dashboard)
- **JSON Telemetry API**: [http://127.0.0.1:5000/api/stats](http://127.0.0.1:5000/api/stats)

---

## 📁 Project Structure

```
cloud honeypot-monitor/
├── app.py                      # Flask backend, honeypot traps & routes
├── requirements.txt            # Python dependencies (Flask)
├── README.md                   # Project documentation
└── templates/                  # Frontend HTML templates
    ├── index.html              # System landing & overview page
    ├── login.html              # Decoy enterprise login page
    └── dashboard.html          # SOC attack telemetry dashboard
```

---

## 🧪 How It Works

1. **Decoy Gateway**: A simulated enterprise cloud console login (`/login`) acts as a decoy honeypot.
2. **Telemetry Capture**: When credentials are submitted:
   - Attempted **username** is recorded.
   - Client **IP address** and **User-Agent** are extracted.
   - Timestamp is generated.
   - **Password is discarded immediately**.
   - Attempt counter increments.
3. **SOC Dashboard**: Displays the total count of failed login attempts, unique targeted usernames, client host IPs, and an event log table.
