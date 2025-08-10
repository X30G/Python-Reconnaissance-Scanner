# Python-Reconnaissance-Scanning
Python recon and scanning using nmap

# Smart Recon & Scanning Tool

[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Pentesting](https://img.shields.io/badge/category-pentesting-red.svg)]()
[![Made With](https://img.shields.io/badge/made%20with-Nmap-orange.svg)](https://nmap.org/)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey.svg)]()
[![Warning](https://img.shields.io/badge/warning-Authorized%20Testing%20Only-critical.svg)](#⚠️-disclaimer)

---

## 📌 Purpose
This script automates the reconnaissance and scanning phase of a penetration test by combining **Nmap**, **socket-based banner grabbing**, and **web service analysis**. It intelligently parses scan results to focus on actual open services, making your recon more accurate and efficient.

---

## 📖 Description
The Smart Recon & Scanning Tool:
- Runs a **full-port Nmap scan** with service/version detection.
- Parses the Nmap **XML output** to find actual open services.
- Uses **socket** to grab banners from non-web services.
- Uses **Requests** + **BeautifulSoup** to analyze discovered web pages for titles and metadata.
- Supports **verbose mode** for detailed feedback or quiet mode for clean output.
- Saves results in both **TXT** and **XML** formats for later review or reporting.

---

## 🚀 Features
- **Smart Targeting** – Only analyzes services that Nmap finds open.
- **Web Recon** – Automatically identifies and inspects HTTP/HTTPS services.
- **Banner Grabbing** – Quickly identifies non-web services via `socket`.
- **Cross-Platform** – Runs on Linux, macOS, and Windows (with Python 3 + Nmap installed).
- **Output Files** – Saves detailed scan results in `nmap_scan_<timestamp>.txt` and `.xml`.
- **Verbose/Quiet Modes** – Toggle detailed output as needed.

---

## 🛠 Requirements
- **Python 3.7+**
- **Nmap** installed and accessible in PATH
- Python modules:
```
  pip install requests beautifulsoup4
```
---

## 💡 Example Usage
```Run with verbose output (default)
python3 python_recon.py <target>
python3 python_recon.py x.x.x.x

Run in quiet mode:
python3 python_recon.py <target> --quiet
```
---

## 📜 Example Output (Verbose Mode)
```
============================================================
   Smart Recon & Scanning Tool
============================================================
[+] Running Nmap scan on x.x.x.x...
[+] Scan complete! XML: nmap_scan_20250809_143000.xml, TXT: nmap_scan_20250809_143000.txt
[+] x.x.x.x - http (Apache httpd 2.4.51)
    [Web] Fetching: http://x.x.x.x:80
    [Web] Title: Example_Domain.com
    [Web] Meta: description = This is an example website.
[+] x.x.x.x:22 - ssh (OpenSSH 8.2)
    [Banner] SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3
[+] Detailed scan saved to: nmap_scan_20250809_143000.txt
```
---

## ⚠️ Disclaimer
This tool is intended solely for educational purposes and authorized penetration testing.
You are responsible for ensuring you have explicit permission from the system owner before running this script against any target.
Unauthorized use of this tool against networks, systems, or applications without prior consent may be illegal and could result in criminal charges.
The author assumes no liability for any misuse or damage caused by this software.
