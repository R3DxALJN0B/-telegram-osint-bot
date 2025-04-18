#!/usr/bin/env python3
import sys
import requests

def lookup_number(number):
    print(f"[+] Looking up number: {number}")
    url = f"https://numverify.com/validate?number={number}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("[+] Request successful.")
            print(response.text)
        else:
            print(f"[-] Failed to fetch data. Status code: {response.status_code}")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 phoneinfoga.py <phonenumber>")
        sys.exit(1)
    lookup_number(sys.argv[1])
