# 🛡️ NakulaScan v2.6 - Red Team Stealth Recon Tool

**NakulaScan** is a precision-crafted, stealth-optimized reconnaissance tool built for Red Team operations, CTF challenges, and cybersecurity mastery.

Inspired by the warrior Nakula — precise, silent, and deeply disciplined — this tool is designed for clean execution, low detection, and high clarity.

---

## 🌟 Features

- ✅ Asynchronous TCP scanning with threading
- ✅ **FIN / NULL / XMAS** stealth scan modes (NEW in v2.6)
- ✅ TTL randomization for passive OS fingerprint obfuscation
- ✅ Threaded banner grabbing for service detection
- ✅ Output: JSON report with port, banner, guessed OS, and scan type
- ✅ Operator codename + CLI with optional ASCII banner
- ✅ Clean CLI output with optional `--nobanner` flag

---

## ⚡ Quick Start

### 🔹 Scan a Single Target (Common Ports)

```bash
sudo python3 nakulascan.py -t 192.168.1.5
🔹 Scan Multiple Targets from a File
bash
Copy
Edit
sudo python3 nakulascan.py -T targets.txt -p full
🔐 Stealth Scan Modes (v2.6)
Use stealthy TCP packet scans that avoid full handshakes, ideal for evading IDS/IPS.


Scan Mode	Description
--scan fin	Sends TCP packets with only the FIN flag
--scan null	Sends TCP packets with no flags
--scan xmas	Sends FIN + PSH + URG flags (XMAS tree scan)
Example:
bash
Copy
Edit
sudo python3 nakulascan.py -t 10.10.10.5 -p common --scan fin
🧠 Passive OS Guessing
TTL of 64 → Linux

TTL of 128 → Windows

Result shown inline and in JSON output

📄 Output Sample (JSON)
json
Copy
Edit
{
  "ip": "192.168.1.5",
  "port": 22,
  "status": "open",
  "service": "SSH",
  "banner": "OpenSSH_8.2p1 Ubuntu",
  "os_guess": "Linux",
  "scan_type": "FIN"
}
📁 Example Target File
Just a simple list:

Copy
Edit
192.168.1.1
10.10.10.10
scanme.nmap.org
🛠️ Usage Flags Summary

Flag	Description
-t	Target IP or hostname
-T	File of multiple targets
-p	common or full ports
--scan	Stealth mode: fin, null, or xmas
--nobanner	Disable ASCII banner output
🧭 Philosophy
"He who moves without being seen is the truest warrior." — Nakula

NakulaScan prioritizes:

🕶️ Stealth over speed

🎯 Precision over chaos

💡 Discipline over noise

🛡️ License
MIT License
This tool is for ethical and educational use only.

🔥 Closing Thought
True strength lies not in noise — but in silent mastery.
“ॐ Tat Sat.” — Nakula