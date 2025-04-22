# NakulaScan
🛡️ **NakulaScan - Stealth Reconnaissance Platform**

NakulaScan is a lightweight, stealth-optimized reconnaissance tool designed for ethical Red Team operations, CTF challenges, and cybersecurity learning.  
It blends intelligent stealth scanning with clean reporting and adaptive behaviors to survive real-world network defenses.

---

## 🌟 Features

- ✅ Asynchronous multi-target TCP & UDP stealth scanning
- ✅ Whisper, Stealth, Fast, Aggressive speed profiles
- ✅ Automatic packet fragmentation option
- ✅ Passive OS fingerprinting (TTL analysis)
- ✅ Banner grabbing from open services
- ✅ Crash-resilient autosaving mid-scan
- ✅ Beautiful HTML, Markdown, and JSON report generation
- ✅ Operator codename generation for session tracking
- ✅ Colorized CLI with nested progress bars
- ✅ Adaptive stealth behaviors (dynamic timing, packet noise)

---

## ⚡ Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/NakulaScan.git
   cd NakulaScan/core
Install requirements:

bash
Copy
Edit
pip install tqdm scapy
Example stealth scan:

bash
Copy
Edit
sudo python3 nakulascan.py -t 192.168.1.5 -p common -s stealth
Example multi-target scan:

bash
Copy
Edit
sudo python3 nakulascan.py -T ../examples/targets.txt -p full -s whisper
View generated reports under:

bash
Copy
Edit
/reports/
🛡️ Usage Options

Option	Description
-t / --target	Single target IP or hostname
-T / --targetlist	File containing list of targets
-p / --ports	Port set: common, full, or custom (22,80,443)
-c / --custom	Comma-separated ports (if -p custom)
-s / --speed	Scan speed: whisper, stealth, fast, aggressive
-u / --udp	Include UDP scan (optional)
-f / --fragment	Enable packet fragmentation for stealth
🧠 Philosophy
"He who moves without being seen is the truest warrior." — Nakula

NakulaScan is designed with the Red Team mindset:

Patience > Speed

Stealth > Noise

Precision > Chaos

Intelligence > Brute Force

Built to survive real-world defenses while maintaining operator integrity.

📚 Example Target File
Example targets.txt:

Copy
Edit
192.168.1.5
10.10.10.10
scanme.nmap.org
Place your targets in a simple list, one per line.

📈 Future Expansion Roadmap
✨ Advanced OS fingerprinting engine (expand on TTL/WindowSize)

✨ Integrated vulnerability suggestion mode (offline CVE matching)

✨ Scan resume from JSON state files

✨ Full HTML dashboard reporting

🔥 Operator Closing Thought
NakulaScan is a reminder:
True strength lies not in noise — but in silent mastery.
Stay disciplined. Move wisely. Remain unseen.

🛡️ License
This project is licensed under the MIT License.
For ethical and educational purposes only.

