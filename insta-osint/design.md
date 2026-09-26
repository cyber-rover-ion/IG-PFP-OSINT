# Insta-OSINT: PFP Getter

A simple, educational Python tool to retrieve public profile picture URLs from Instagram. Designed to run on Kali Linux, Termux (Android), and standard Python environments.

> **Disclaimer:** This tool only works on **PUBLIC** accounts. Using this on private accounts requires authentication, which is not included here to prevent account bans. For educational purposes only.

## Features
- ✅ Cross-platform (Linux, Android/Termux, Windows, macOS)
- ✅ Retrieves High-Resolution Profile Pictures (if public)
- ✅ No external API keys required
- ✅ CLI-based with color output

## Installation

### Option 1: Kali Linux / Parrot OS / Ubuntu
```bash
sudo apt update
sudo apt install python3 python3-pip git
git clone <YOUR_REPO_URL_HERE>
cd insta-osint
pip3 install -r requirements.txt