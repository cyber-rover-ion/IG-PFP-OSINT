#!/usr/bin/env python3
import requests
import re
import json
import argparse
import sys
import os

# Colors for CLI output (Works on Kali, Termux, and modern terminals)
class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

def banner():
    print(f"""{Colors.CYAN}
  ___  _   _  ___  _   _  _   _  _   _ 
 / _ \| \ | |/ _ \| \ | |(_) | |(_) | |
| | | |  \| | | | |  \| | _  | | _  | |
| | | | . ` | | | | . ` || | | || | | |
| |_| | |\  | |_| | |\  || | |_| || | |
 \___/|_| \_|\___/|_| \_|/|_|\___/ |_| |
                                       
{Colors.WHITE}Instagram PFP Getter (Educational Use Only)
{Colors.YELLOW}Warning: Only works on PUBLIC accounts.
{Colors.RESET}""")

def get_pfp(username):
    url = f"https://www.instagram.com/{username}/"
    
    # Mimicking a standard browser to avoid immediate blocking
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    print(f"{Colors.BLUE}[*] Targeting: {username}{Colors.RESET}")
    print(f"{Colors.BLUE}[*] Attempting to fetch public data...{Colors.RESET}")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 404:
            print(f"{Colors.RED}[!] Error 404: User '{username}' not found.{Colors.RESET}")
            return
        if response.status_code == 403:
            print(f"{Colors.RED}[!] Error 403: Access Forbidden. Instagram blocked the request.{Colors.RESET}")
            return
        if "Sorry, this page isn't available" in response.text:
            print(f"{Colors.RED}[!] Error: This page is unavailable or the account is private/banned.{Colors.RESET}")
            return

        # Extract JSON data
        match = re.search(r'window._sharedData = (.*);', response.text)
        if not match:
            print(f"{Colors.RED}[!] Error: Could not parse Instagram data. They may have updated their security.{Colors.RESET}")
            return

        data = json.loads(match.group(1))
        user_data = data['entry_data']['ProfilePage'][0]['graphql']['user']

        if user_data['is_private']:
            print(f"{Colors.YELLOW}[!] Warning: Account is PRIVATE.{Colors.RESET}")
            print(f"{Colors.YELLOW}[!] Limited data available without authentication (which is risky).{Colors.RESET}")
            # Even private accounts sometimes leak the low-res PFP in the initial load, let's check
            pfp_url = user_data.get('profile_pic_url')
            if pfp_url:
                print(f"{Colors.GREEN}[+] Found Low-Res PFP (Private Account):{Colors.RESET}")
                print(pfp_url)
            return

        # Extract HD PFP
        hd_pfp_url = None
        if 'hd_profile_pic_url_info' in user_data and user_data['hd_profile_pic_url_info']:
            hd_pfp_url = user_data['hd_profile_pic_url_info']['url']
        
        pfp_url = user_data.get('profile_pic_url')

        print(f"\n{Colors.GREEN}[+] SUCCESS: Data retrieved for @{username}{Colors.RESET}")
        
        if hd_pfp_url:
            print(f"{Colors.GREEN}[+] High-Resolution PFP URL:{Colors.RESET}")
            print(f"{Colors.CYAN}{hd_pfp_url}{Colors.RESET}")
            print(f"\n{Colors.WHITE}You can copy this URL or download it using: \n  curl -o pfp.jpg '{hd_pfp_url}'{Colors.RESET}")
        elif pfp_url:
            print(f"{Colors.YELLOW}[+] Standard PFP URL (HD not available):{Colors.RESET}")
            print(f"{Colors.CYAN}{pfp_url}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] No profile picture found.{Colors.RESET}")

    except json.JSONDecodeError:
        print(f"{Colors.RED}[!] Error: Failed to decode data. Instagram might be serving a CAPTCHA.{Colors.RESET}")
    except KeyError as e:
        print(f"{Colors.RED}[!] Error: Data structure mismatch. Instagram may have changed their code.{Colors.RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}[!] Network Error: {e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[!] Unexpected Error: {e}{Colors.RESET}")

def main():
    banner()
    parser = argparse.ArgumentParser(description="Instagram PFP Getter (Educational)")
    parser.add_argument('-u', '--username', type=str, help='Target Instagram username')
    
    args = parser.parse_args()

    if not args.username:
        print(f"{Colors.RED}[!] Usage: python main.py -u <username>{Colors.RESET}")
        print(f"{Colors.WHITE}Example: python main.py -u instagram{Colors.RESET}")
        sys.exit(1)

    get_pfp(args.username)

if __name__ == "__main__":
    main()
