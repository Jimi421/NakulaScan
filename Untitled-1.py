#!/usr/bin/env python3
# NakulaScan - Stealth Reconnaissance Platform

import asyncio
import argparse
import socket
import random
import json
import os
from tqdm import tqdm
from datetime import datetime
from scapy.all import IP, TCP, UDP, sr1, fragment

# CLI Colors
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Dynamic Codename
def generate_codename():
    names = ["SilentFalcon", "ShadowWolf", "PhantomEagle", "DarkCobra", "SwiftViper"]
    return random.choice(names) + str(random.randint(10, 99))

codename = generate_codename()
scan_start_time = datetime.now()

# Print Banner
print(f"{CYAN}[+] Operator Codename: {codename} {RESET}")
print(f"{CYAN}[+] Tip: Run with -h or --help to see full usage instructions! {RESET}\n")

# Argument Parser
parser = argparse.ArgumentParser(
    description=f"NakulaScan - Stealth Recon ({codename})",
    epilog="""
🛡️ Quick Usage Examples:

▶️ Scan one target stealthily:
    python3 nakulascan.py -t 192.168.1.5 -p common -s stealth

▶️ Scan multiple targets from a file:
    python3 nakulascan.py -T examples/targets.txt -p custom -c 22,80,443 -s fast

▶️ Whisper Mode for extreme stealth:
    python3 nakulascan.py -t 10.10.10.10 -p full -s whisper
"""
)
target_group = parser.add_mutually_exclusive_group(required=True)
target_group.add_argument("-t", "--target", help="Target IP address or hostname")
target_group.add_argument("-T", "--targetlist", help="File containing list of targets")

parser.add_argument("-p", "--ports", default="common", help="Ports to scan: common, full, or comma-separated (22,80,443)")
parser.add_argument("-c", "--custom", help="Custom ports (if -p custom is selected)")
parser.add_argument("-s", "--speed", choices=["whisper", "stealth", "fast", "aggressive"], default="stealth", help="Scan speed profile")
parser.add_argument("-u", "--udp", action="store_true", help="Include UDP scanning")
parser.add_argument("-f", "--fragment", action="store_true", help="Enable packet fragmentation for stealth")

args = parser.parse_args()

# Stealth Timing Profiles
speed_profiles = {
    "whisper": (5.0, 10.0),
    "stealth": (0.5, 2.0),
    "fast": (0.2, 0.5),
    "aggressive": (0.05, 0.2)
}
timeout, delay_range = {
    "whisper": (10, (5.0, 10.0)),
    "stealth": (2, (0.5, 2.0)),
    "fast": (1, (0.2, 0.5)),
    "aggressive": (0.5, (0.05, 0.2))
}[args.speed]

# Port Set
if args.ports == "common":
    ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3389, 8080]
elif args.ports == "full":
    ports = list(range(1, 1025))
elif args.ports == "custom":
    if args.custom:
        ports = [int(p.strip()) for p in args.custom.split(',')]
    else:
        print(f"{RED}[-] Custom ports selected but none provided.{RESET}")
        exit()
else:
    ports = [int(p.strip()) for p in args.ports.split(',')]

# Load Targets
targets = []
if args.target:
    targets.append(args.target)
elif args.targetlist:
    try:
        with open(args.targetlist, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{RED}[-] Failed to load targets file: {e}{RESET}")
        exit()

# Resolve Hostnames
resolved_targets = []
for target in targets:
    try:
        ip = socket.gethostbyname(target)
        resolved_targets.append(ip)
    except socket.gaierror:
        print(f"{RED}[-] Failed to resolve: {target}{RESET}")

if not resolved_targets:
    print(f"{RED}[-] No valid targets to scan. Exiting.{RESET}")
    exit()

# Banner Grabber
def grab_banner(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(2)
        sock.connect((ip, port))
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner if banner else "No Banner"
    except:
        return "No Banner"

# Passive OS Guess (TTL Analysis)
def guess_os(ttl_val):
    if ttl_val <= 64:
        return "Linux/Unix-like"
    elif ttl_val <= 128:
        return "Windows"
    elif ttl_val <= 255:
        return "Cisco/Network Device"
    return "Unknown"

# TCP Scan Function
async def tcp_scan(ip, port):
    pkt = IP(dst=ip, ttl=random.randint(48, 128)) / TCP(dport=port, sport=random.randint(1024,65535), flags="S")
    if args.fragment:
        pkt = fragment(pkt)
    response = sr1(pkt, timeout=timeout, verbose=0)
    await asyncio.sleep(random.uniform(*delay_range))

    if response and response.haslayer(TCP):
        flags = response.getlayer(TCP).flags
        if flags == 0x12:
            banner = grab_banner(ip, port)
            os_guess = guess_os(response.ttl) if hasattr(response, 'ttl') else "Unknown"
            print(f"{GREEN}[+] {ip}:{port} OPEN - {banner} [{os_guess}]{RESET}")
            return {"target": ip, "port": port, "protocol": "tcp", "status": "open", "banner": banner, "os_guess": os_guess}
    return None

# UDP Scan Function
async def udp_scan(ip, port):
    pkt = IP(dst=ip, ttl=random.randint(48, 128)) / UDP(dport=port, sport=random.randint(1024,65535))
    if args.fragment:
        pkt = fragment(pkt)
    response = sr1(pkt, timeout=timeout, verbose=0)
    await asyncio.sleep(random.uniform(*delay_range))

    if not response:
        print(f"{GREEN}[+] {ip}:{port} UDP OPEN or FILTERED{RESET}")
        return {"target": ip, "port": port, "protocol": "udp", "status": "open/filtered"}
    return None

# Scan Function
async def scan_target(ip):
    tasks = []
    for port in ports:
        tasks.append(asyncio.create_task(tcp_scan(ip, port)))
        if args.udp:
            tasks.append(asyncio.create_task(udp_scan(ip, port)))
    results = []
    for f in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc=f"Scanning {ip}", ncols=70):
        result = await f
        if result:
            results.append(result)
    return results

# Report Writers
def write_json_report(results):
    folder = f"reports/{scan_start_time.strftime('%Y-%m-%d')}_{codename}"
    os.makedirs(folder, exist_ok=True)
    with open(f"{folder}/scan_results.json", "w") as f:
        json.dump(results, f, indent=2)

def write_markdown_report(results):
    folder = f"reports/{scan_start_time.strftime('%Y-%m-%d')}_{codename}"
    os.makedirs(folder, exist_ok=True)
    with open(f"{folder}/scan_results.md", "w") as f:
        f.write(f"# NakulaScan Report - {codename}\n")
        f.write(f"**Date:** {scan_start_time}\n\n")
        for r in results:
            f.write(f"- {r['target']}:{r['port']} ({r['protocol']}) - {r['status']} - {r['banner']} - {r['os_guess']}\n")

def write_html_report(results):
    folder = f"reports/{scan_start_time.strftime('%Y-%m-%d')}_{codename}"
    os.makedirs(folder, exist_ok=True)
    with open(f"{folder}/scan_results.html", "w") as f:
        f.write(f"<html><head><title>NakulaScan Report</title></head><body>")
        f.write(f"<h1>NakulaScan Report - {codename}</h1>")
        f.write(f"<h2>Scan Date: {scan_start_time}</h2><table border='1'><tr><th>Target</th><th>Port</th><th>Protocol</th><th>Status</th><th>Banner</th><th>OS Guess</th></tr>")
        for r in results:
            f.write(f"<tr><td>{r['target']}</td><td>{r['port']}</td><td>{r['protocol']}</td><td>{r['status']}</td><td>{r['banner']}</td><td>{r['os_guess']}</td></tr>")
        f.write("</table><br><em>Om Tat Sat - Stealth in Honor of Nakula.</em></body></html>")

# Main
async def main():
    all_results = []
    for ip in resolved_targets:
        print(f"{CYAN}[+] Beginning scan on {ip}...{RESET}")
        target_results = await scan_target(ip)
        all_results.extend(target_results)
    if all_results:
        write_json_report(all_results)
        write_markdown_report(all_results)
        write_html_report(all_results)
        print(f"{CYAN}[+] Reports saved successfully.{RESET}")
    else:
        print(f"{RED}[-] No open ports detected.{RESET}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
        print(f"\n{CYAN}[*] NakulaScan Complete. {RESET}")
        print(f"{CYAN}[*] 'He who moves without being seen is the truest warrior.' - Nakula {RESET}")
    except KeyboardInterrupt:
        print(f"\n{RED}[-] Scan aborted by user.{RESET}")
