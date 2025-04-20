# 🛡️ NakulaScan - Red Team Stealth Recon Tool

---

## 🌟 What is NakulaScan?

NakulaScan is a professional-grade stealth port scanner and recon platform inspired by Nakula, the master of subtle warfare from the Mahabharata.

Built for real Red Team operations:
- Stealth SYN/FIN/XMAS scans
- Micro-random timing drift
- Target pre-check health scan
- Packet fragmentation option
- Codename generation for op tracking
- Mid-scan autosave resilience
- Clean CLI help system with examples

Victory loves preparation. 🔥

---

## ⚙️ Requirements

- Python 3
- Scapy:
  ```bash
  pip3 install scapy
  ```
- (Optional) Proxychains for TOR routing.

---

## 🚀 Quick Usage Examples

---

👉 **Scan one target stealthily:**
```bash
sudo python3 nakula_scan_core.py -t 192.168.1.5 -p common -s stealth -scan syn
```

👉 **Scan multiple targets from a file:**
```bash
sudo python3 nakula_scan_core.py -T targets.txt -p full -s fast -scan syn
```

👉 **Custom ports scan (22, 80, 443):**
```bash
sudo python3 nakula_scan_core.py -t 10.10.10.5 -p custom -c 22,80,443 -s stealth -scan xmas
```

👉 **Fragment packets for stealth bypass:**
```bash
sudo python3 nakula_scan_core.py -t 192.168.1.1 -frag
```

👉 **Scan over TOR (Proxychains):**
```bash
proxychains4 sudo python3 nakula_scan_core.py -t scanme.nmap.org -p common -s stealth -scan syn
```

👉 **Show full help menu and examples:**
```bash
sudo python3 nakula_scan_core.py -h
```

Use `-h` or `--help` anytime to view all options, modes, and usage examples directly in your terminal.

---

## 📦 Project Layout

```
NakulaScan/
├── nakula_scan_core.py
├── README.md
├── targets.txt
├── Roadmap.md
├── .gitignore
├── LICENSE (optional)
├── outputs/
```

---

## 🧐 Key Features

| Feature | Description |
|:--------|:------------|
| Stealth Modes | SYN, FIN, XMAS |
| Speed Profiles | Stealth, Fast, Aggressive |
| Health Checks | Ping sweep live hosts |
| Codename Ops | Auto codename for every scan session |
| Fragmentation | Bypass DPI / Firewall detection |
| Autosave | Mid-scan and final autosave JSON |
| Clean CLI Help | Built-in examples for fast start |

---

## 💪 Final Thought

_"Silent as the moon, swift as the wind — this is the way of the wise."_ — Nakula (Mahabharata)

Victory loves preparation. 🔥

---

**Built by Red Teamers. For Red Teamers. 🛡️🔥**

