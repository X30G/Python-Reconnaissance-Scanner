#!/usr/bin/env python3
"""
Recon & Scanning Tool
- Uses Nmap for deep scanning with XML output
- Parses scan results to find web services
- Requests + BeautifulSoup for web recon
- Verbose mode for detailed feedback
"""

import subprocess
import sys
import datetime
import shutil
import socket
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup

# Verbose
VERBOSE = True   # Set to False for quieter output
TIMEOUT = 5      # Seconds for socket/web timeouts

def vprint(msg):
    """Verbose print helper"""
    if VERBOSE:
        print(msg)

def banner():
    print("=" * 60)
    print("   Smart Recon & Scanning Tool   ")
    print("=" * 60)

def run_nmap(target):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    xml_file = f"nmap_scan_{timestamp}.xml"
    txt_file = f"nmap_scan_{timestamp}.txt"

    command = [
        "nmap",
        "-sV",
        "-T4",
        "-p-",
        "-oX", xml_file,
        "-oN", txt_file,
        target
    ]

    vprint(f"[+] Running Nmap scan on {target}...")
    subprocess.run(command)
    vprint(f"[+] Scan complete! XML: {xml_file}, TXT: {txt_file}")

    return xml_file, txt_file

def parse_nmap_xml(xml_file):
    """Parse Nmap XML and return list of services"""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    services = []
    for host in root.findall("host"):
        addr = host.find("address").get("addr")
        for port in host.find("ports").findall("port"):
            port_num = port.get("portid")
            state = port.find("state").get("state")
            service_el = port.find("service")
            if service_el is not None:
                name = service_el.get("name", "")
                product = service_el.get("product", "")
                version = service_el.get("version", "")
            else:
                name = product = version = ""

            if state == "open":
                services.append({
                    "ip": addr,
                    "port": int(port_num),
                    "service": name,
                    "product": product,
                    "version": version
                })
    return services

def quick_banner_grab(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        s.connect((target, port))
        banner = s.recv(1024).decode(errors="ignore").strip()
        s.close()
        return banner
    except Exception:
        return None

def web_recon(url):
    try:
        vprint(f"    [Web] Fetching: {url}")
        response = requests.get(url, timeout=TIMEOUT)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "No title found"
        print(f"    [Web] Title: {title}")
        for meta in soup.find_all("meta"):
            name = meta.get("name") or meta.get("property")
            content = meta.get("content")
            if name and content:
                vprint(f"    [Web] Meta: {name} = {content}")
    except Exception as e:
        print(f"    [Web] Could not fetch {url} - {e}")

def main():
    global VERBOSE
    banner()

    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <target> [--quiet]")
        sys.exit(1)

    target = sys.argv[1]
    if "--quiet" in sys.argv:
        VERBOSE = False

    if not shutil.which("nmap"):
        print("[!] Nmap is not installed. Please install it and try again.")
        sys.exit(1)

# Run Nmap and get XML + TXT output
    xml_file, txt_file = run_nmap(target)

# Parse Nmap results
    services = parse_nmap_xml(xml_file)

# Process results
    for svc in services:
        print(f"[+] {svc['ip']}:{svc['port']} - {svc['service']} ({svc['product']} {svc['version']})")

# Banner grab for non-HTTP
        if svc['service'] not in ["http", "https"]:
            banner_data = quick_banner_grab(svc['ip'], svc['port'])
            if banner_data:
                vprint(f"    [Banner] {banner_data}")

# Web recon for HTTP(S)
        if svc['service'] in ["http", "https"]:
            proto = "https" if svc['service'] == "https" or svc['port'] == 443 else "http"
            web_recon(f"{proto}://{svc['ip']}:{svc['port']}")

    print(f"[+] Detailed scan saved to: {txt_file}")

if __name__ == "__main__":
    main()
