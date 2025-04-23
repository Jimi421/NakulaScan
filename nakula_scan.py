# NakulaScan v2.6 - Stealth Engine Core

import argparse
import socket
import random
import threading
import time
import json
from datetime import datetime
from scapy.all import *

conf.verb = 0

# Color definitions
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Port to service mapping
PORT_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 139: "SMB",
    143: "IMAP", 443: "HTTPS", 445: "SMB", 3306: "MySQL",
    3389: "RDP", 8080: "HTTP-Alt", 8443: "HTTPS-Alt"
}

# ASCII Banner
ASCII_BANNER = f"""
{CYAN}
███╗   ██╗ █████╗ ██╗  ██╗██╗   ██╗██╗      █████╗ 
████╗  ██║██╔══██╗██║ ██╔╝██║   ██║██║     ██╔══██╗
██╔██╗ ██║███████║█████╔╝ ██║   ██║██║     ███████║
██║╚██╗██║██╔══██║██╔═██╗ ██║   ██║██║     ██╔══██║
██║ ╚████║██║  ██║██║  ██╗╚██████╔╝███████╗██║  ██║
╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝

        ॐ  (Om - Sacred Operator Mind)
{RESET}v2.6 - Red Team Stealth Recon Tool
"""

# Codename generator
def generate_codename():
    names = ["SilentFalcon", "GhostTiger", "ShadowWolf", "PhantomEagle", "SwiftViper", "DarkCobra"]
    return random.choice(names) + str(random.randint(10,99))

# Banner grabbing function
def grab_banner(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=1) as s:
            s.settimeout(1)
            banner = s.recv(1024).decode(errors='ignore').strip()
            return banner
    except:
        return ""

# TTL-based OS guessing
def guess_os(ttl):
    if ttl >= 128:
        return "Windows"
    elif ttl >= 64:
        return "Linux"
    else:
        return "Unknown"

# Stealth scan engine (FIN/NULL/XMAS)
def stealth_tcp_scan(ip, port, scan_type):
    flags_map = {
        "fin": "F",
        "null": "",
        "xmas": "FPU"
    }
    try:
        pkt = IP(dst=ip, ttl=random.randint(32,128))/TCP(dport=port, flags=flags_map[scan_type.lower()])
        response = sr1(pkt, timeout=1, verbose=0)
        if response is None:
            return True  # Open (silent)
        elif response.haslayer(TCP) and response.getlayer(TCP).flags == 0x14:
            return False  # Closed
    except:
        pass
    return None

# Argument parser
parser = argparse.ArgumentParser(description="NakulaScan - Stealth Recon Platform")
parser.add_argument("-t", "--target", help="Target IP or hostname")
parser.add_argument("-T", "--targetlist", help="File containing list of targets")
parser.add_argument("-p", "--ports", choices=["common", "full"], default="common", help="Port set")
parser.add_argument("--scan", choices=["fin", "null", "xmas"], help="Stealth scan mode")
parser.add_argument("--nobanner", action="store_true", help="Suppress ASCII banner")
args = parser.parse_args()

if not args.nobanner:
    print(ASCII_BANNER)

codename = generate_codename()
print(f"{CYAN}[+] Operator Codename: {codename}{RESET}")

# Load targets
if args.targetlist:
    with open(args.targetlist, 'r') as f:
        targets = [line.strip() for line in f if line.strip()]
elif args.target:
    targets = [args.target]
else:
    print(f"{RED}[-] No targets specified.{RESET}")
    exit()

# Port sets
if args.ports == "common":
    ports = list(PORT_SERVICES.keys())
elif args.ports == "full":
    ports = list(range(1, 1025))

# Results
results = []
print_lock = threading.Lock()

def scan_target(ip):
    print(f"\n{CYAN}[+] Scanning {ip}...{RESET}")
    try:
        ans = sr1(IP(dst=ip)/ICMP(), timeout=1, verbose=0)
        ttl = ans.ttl if ans else 0
        os_guess = guess_os(ttl)
    except:
        os_guess = "Unknown"

    for port in ports:
        try:
            status = None
            if args.scan:
                status = stealth_tcp_scan(ip, port, args.scan)
                if status is None:
                    continue
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                result = s.connect_ex((ip, port))
                status = result == 0
                s.close()

            if status:
                service = PORT_SERVICES.get(port, "Unknown")
                banner = grab_banner(ip, port) if not args.scan else ""
                with print_lock:
                    print(f"{GREEN}[+] {ip}:{port} OPEN ({service}) [{os_guess}] ({args.scan.upper() if args.scan else 'CONNECT'}){RESET}")
                results.append({
                    "ip": ip,
                    "port": port,
                    "status": "open",
                    "service": service,
                    "banner": banner,
                    "os_guess": os_guess,
                    "scan_type": args.scan.upper() if args.scan else "CONNECT"
                })
        except:
            continue

# Start threads
threads = []
for target in targets:
    t = threading.Thread(target=scan_target, args=(target,))
    t.start()
    threads.append(t)
    time.sleep(0.1)

for t in threads:
    t.join()

# Save results
with open("nakulascan_results.json", "w") as f:
    json.dump(results, f, indent=4)

print(f"\n{CYAN}[+] Scan complete. Results saved to nakulascan_results.json{RESET}")
