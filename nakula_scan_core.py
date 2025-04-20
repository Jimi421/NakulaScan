# NAKULASCAN PLATFORM - FINAL UPGRADED CORE WITH CLEAN USAGE EXAMPLES

import argparse
import socket
import random
import threading
import time
import os
import json
from scapy.all import *
from datetime import datetime

conf.verb = 0

# Color definitions
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Codename generator
def generate_codename():
    names = ["SilentFalcon", "GhostTiger", "ShadowWolf", "PhantomEagle", "SwiftViper", "DarkCobra"]
    return random.choice(names) + str(random.randint(10,99))

codename = generate_codename()

# Print startup info
print(f"{CYAN}[+] Operator Codename: {codename} {RESET}")
print(f"{CYAN}[+] Tip: Run with -h or --help to see usage instructions!{RESET}")

# Argument parser
parser = argparse.ArgumentParser(
    description=f"NakulaScan - Operator Codename: {codename}",
    epilog=f"""
🛡️ Quick Usage Examples
---

▶️ Scan one target stealthily:
    sudo python3 nakula_scan_core.py -t 192.168.1.5 -p common -s stealth -scan syn

▶️ Scan multiple targets from a file:
    sudo python3 nakula_scan_core.py -T targets.txt -p full -s fast -scan syn

▶️ Custom ports scan (22, 80, 443):
    sudo python3 nakula_scan_core.py -t 10.10.10.5 -p custom -c 22,80,443 -s stealth -scan xmas

▶️ Fragment packets for stealth bypass:
    sudo python3 nakula_scan_core.py -t 192.168.1.1 -frag

▶️ Scan over TOR (Proxychains):
    proxychains4 sudo python3 nakula_scan_core.py -t scanme.nmap.org -p common -s stealth -scan syn
"""
)

parser.add_argument("-t", "--target", help="Target IP or hostname")
parser.add_argument("-T", "--targetlist", help="File containing list of targets")
parser.add_argument("-p", "--ports", choices=["common", "full", "custom"], default="common", help="Port set")
parser.add_argument("-c", "--custom", help="Custom ports list (comma separated)")
parser.add_argument("-s", "--speed", choices=["stealth", "fast", "aggressive"], default="stealth", help="Scan speed")
parser.add_argument("-scan", "--scan_type", choices=["syn", "fin", "xmas"], default="syn", help="Scan type")
parser.add_argument("-frag", "--fragment", action="store_true", help="Fragment packets for stealth")

args = parser.parse_args()

# Load targets
if args.targetlist:
    with open(args.targetlist, 'r') as f:
        targets = [line.strip() for line in f if line.strip()]
elif args.target:
    targets = [args.target]
else:
    print(f"{RED}[-] No targets specified.{RESET}")
    exit()

# Pre-scan: Health check (ICMP ping)
print(f"{CYAN}[+] Performing target availability checks...{RESET}")

live_targets = []  # Hold dictionaries with hostname + IP
unresolved_targets = []

for target in targets:
    try:
        ip = socket.gethostbyname(target)
        ans = sr1(IP(dst=ip)/ICMP(), timeout=1, verbose=0)
        if ans:
            live_targets.append({"hostname": target, "ip": ip})
        else:
            unresolved_targets.append(target)
    except:
        unresolved_targets.append(target)

# Save unresolved hosts
if unresolved_targets:
    with open("unresolved.txt", "w") as f:
        for u in unresolved_targets:
            f.write(u + "\n")
    print(f"{RED}[-] {len(unresolved_targets)} hosts unreachable. Saved to unresolved.txt.{RESET}")

if not live_targets:
    print(f"{RED}[-] No live targets found. Exiting.{RESET}")
    exit()

# Port set
if args.ports == "common":
    ports = [21,22,23,25,53,80,110,135,139,143,443,445,3389,8080,8443,3306,1433,5900,5060]
elif args.ports == "full":
    ports = list(range(1, 1025))
elif args.ports == "custom":
    if not args.custom:
        print(f"{RED}[-] Custom ports specified but no list given.{RESET}")
        exit()
    ports = [int(port.strip()) for port in args.custom.split(',')]

# Speed profiles
if args.speed == "stealth":
    timeout_range = (0.5, 1.5)
    sleep_range = (0.3, 0.7)
elif args.speed == "fast":
    timeout_range = (0.2, 0.5)
    sleep_range = (0.05, 0.15)
elif args.speed == "aggressive":
    timeout_range = (0.05, 0.2)
    sleep_range = (0.01, 0.05)

# Scan type
if args.scan_type == "syn":
    scan_flag = "S"
elif args.scan_type == "fin":
    scan_flag = "F"
elif args.scan_type == "xmas":
    scan_flag = "FPU"

# Results holder
scan_results = []
print_lock = threading.Lock()
source_port = random.randint(1024, 65535)

# Stealth scan function
def stealth_scan(target_ip, port):
    try:
        ip = IP(dst=target_ip)
        tcp = TCP(sport=source_port, dport=port, flags=scan_flag)
        pkt = ip/tcp
        if args.fragment:
            pkt = fragment(pkt)
        response = sr1(pkt, timeout=random.uniform(*timeout_range), retry=0)

        if response and response.haslayer(TCP):
            tcp_layer = response.getlayer(TCP)
            if scan_flag == "S" and tcp_layer.flags == 0x12:
                send(IP(dst=target_ip)/TCP(sport=source_port, dport=port, flags="R"))
                with print_lock:
                    print(f"{GREEN}[+] {target_ip}:{port} OPEN{RESET}")
                scan_results.append({"target": target_ip, "port": port, "status": "open"})
            elif scan_flag in ["F", "FPU"] and tcp_layer.flags == 0x14:
                pass
    except Exception:
        pass
    finally:
        time.sleep(random.uniform(*sleep_range) + random.uniform(0.01, 0.05))

# Autosave function
def autosave_results():
    with open("autosave.json", "w") as f:
        json.dump(scan_results, f)

# Main scanning loop
for target_info in live_targets:
    hostname = target_info["hostname"]
    ip = target_info["ip"]
    print(f"\n{CYAN}[+] Scanning {ip} ({hostname}) - Codename: {codename}{RESET}")
    random.shuffle(ports)
    threads = []

    for port in ports:
        t = threading.Thread(target=stealth_scan, args=(ip, port))
        threads.append(t)
        t.start()
        time.sleep(random.uniform(*sleep_range))

    if len(threads) > len(ports)//2:
        autosave_results()

    for t in threads:
        t.join()

# Final save
autosave_results()
print(f"\n{CYAN}[+] Final results saved to autosave.json{RESET}")
print(f"{CYAN}[+] NakulaScan completed. Operated under Codename: {codename}{RESET}")
