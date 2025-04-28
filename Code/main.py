# main.py

import argparse
import os
from datetime import datetime
from utils import validate_ip_or_subnet
from scanner import perform_full_scan, subnet_discovery
from sqlscanner import run_sqlmap
from dirscanner import run_gobuster
from analyzer import analyze_with_deepseek
from exploitscanner import search_exploits
from utils import extract_services
from banner import print_banner

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Otomatik Pentest Aracı")
    parser.add_argument("--target", required=True, help="Hedef IP veya domain")
    parser.add_argument("--api_key", required=True, help="DeepSeek API anahtarı")
    parser.add_argument("--subnet", help="Subnet keşfi için örn: 192.168.1.0/24")
    args = parser.parse_args()

    if not validate_ip_or_subnet(args.target):
        print("[HATA] Geçersiz IP veya subnet!")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("reports", exist_ok=True)

    # Eğer subnet verildiyse keşif yap
    if args.subnet:
        subnet_discovery(args.subnet, f"reports/subnet_scan_{timestamp}.txt")

    # Hedef taraması
    nmap_output_file = f"reports/nmap_results_{timestamp}.txt"
    firewall_detected, open_ports, nmap_results = perform_full_scan(args.target, nmap_output_file)

    # Web servisleri kontrolü
    if any(port in [80, 443, 8080] for port in open_ports):
        protocol = "https" if 443 in open_ports else "http"
        target_url = f"{protocol}://{args.target}"

        run_sqlmap(target_url, firewall_detected, f"reports/sqlmap_{timestamp}.txt")
        run_gobuster(target_url, "/usr/share/wordlists/dirb/common.txt", f"reports/gobuster_{timestamp}.txt")

    # Exploit araştırması
    services = extract_services(nmap_results)
    search_exploits(services, f"reports/exploits_{timestamp}.txt")

    # DeepSeek analizi
    analyze_with_deepseek(args.api_key, nmap_results, f"reports/pentest_report_{timestamp}.txt")

if __name__ == "__main__":
    main()
    
