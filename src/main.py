# main.py
import os
import argparse  
from datetime import datetime
from .core.dependency_checker import check_all_dependencies
from .core.banner import print_banner
from .utils import validate_ip_or_subnet, extract_services # utils da src altında
from .scanner.nmap_scanner import perform_full_scan, subnet_discovery
from .scanner.sql_scanner import run_sqlmap
from .scanner.dir_scanner import run_gobuster
from .analyzer.deepseek_analyzer import analyze_with_deepseek
from .exploit.exploit_db_searcher import search_exploits
from reports.report_generator import handle_reporting
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

    report_target_info = {
        'ip': args.target,
        'url': args.target,
        'scan_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    #Rapor dönüştürme
    handle_reporting(report_target_info, nmap_results, whatweb_results, deepseek_report_content, f"pentest_report_{timestamp}")
    # ----------------------------------------

    print("\n--- Tarama ve Raporlama tamamlandı! ---")

    
if __name__ == "__main__":
    check_all_dependencies()
    main()
   

    
