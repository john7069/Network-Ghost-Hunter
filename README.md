# 👻 Network Ghost Hunter
![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Security](https://img.shields.io/badge/Security-RedTeam-red?style=flat)

**A professional-grade, multi-threaded network reconnaissance tool designed for ethical hacking and vulnerability assessment.**

> *Developed as a collaborative security project.*

## 🚀 Features
* **Turbo-Charged Scanning:** Utilizes `concurrent.futures` to scan 100+ ports simultaneously, reducing scan time by 90% compared to sequential scanners.
* **Smart Service Recon:** Automatically identifies running services (HTTP, SSH, SMB, etc.) using Banner Grabbing and an intelligent fallback dictionary.
* **Legal Compliance Module:** Features a mandatory "Click-Through" agreement that forces users to acknowledge ethical usage policies before the tool executes.
* **Professional TUI:** Includes a "Hacker-style" Text User Interface with live progress animations, color-coded results, and clean data visualization.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)john7069/Network-Ghost-Hunter.git
    cd Network-Ghost-Hunter
    ```

2.  **Install dependencies:**
    This tool uses `colorama` for cross-platform color support.
    ```bash
    pip install colorama
    ```

## 💻 Usage

Run the script from your terminal:
```bash
python port_scanner.py

Follow the on-screen prompts:

Accept the Disclaimer: Type AGREE to confirm you have authorization to scan.

Enter Target: Input the IP address (e.g., 127.0.0.1).

Set Range: Define your start and end ports (e.g., 1 to 1000).
