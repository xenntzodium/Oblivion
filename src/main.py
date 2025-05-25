# main.py
import os
import argparse  
from datetime import datetime
from src.core.dependency_checker import check_all_dependencies
from src.core.banner import print_banner
from src.utils import validate_ip_or_subnet, extract_services 
from src.scanner.nmap_scanner import perform_full_scan, subnet_discovery
from src.scanner.sql_scanner import run_sqlmap
from src.scanner.dir_scanner import run_gobuster
from src.analyzer.deepseek_analyzer import analyze_with_deepseek
from src.exploit.exploit_db_searcher import search_exploits
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
    os.makedirs("reports", exist_ok=True) # Rapor dizini oluşturma

    # Raporlama için kullanılacak başlangıç değerleri
    deepseek_report_content = ""
    target_url = None # Web servis URL'si başlangıçta None (Rapora aktarılacak)

    # Eğer subnet verildiyse keşif yap
    if args.subnet:
        print(f"\n--- Subnet Keşfi ({args.subnet}) ---")
        subnet_discovery(args.subnet, f"reports/subnet_scan_{timestamp}.txt")

    # Hedef taraması
    nmap_output_file = f"reports/nmap_results_{timestamp}.txt"
    # perform_full_scan'dan dönen 3. değer ham Nmap çıktısıdır.
    firewall_detected, open_ports, nmap_raw_output = perform_full_scan(args.target, nmap_output_file)

    # Web servisleri kontrolü ve taramaları (WhatWeb kısmı çıkarıldı)
    if any(port in [80, 443, 8080] for port in open_ports):
        protocol = "https" if 443 in open_ports else "http"
        target_url = f"{protocol}://{args.target}"
        print(f"\n--- Web Servisleri Taraması ({target_url}) ---")

        run_sqlmap(target_url, firewall_detected, f"reports/sqlmap_{timestamp}.txt")
        run_gobuster(target_url, "/usr/share/wordlists/dirb/common.txt", f"reports/gobuster_{timestamp}.txt")
    else:
        print("Web servisleri (80, 443, 8080) bulunamadı. Web taramaları atlanıyor.")


    # Exploit araştırması
    print("\n--- Exploit Araştırması ---")
    # utils.extract_services fonksiyonu ham Nmap çıktısını bekler.
    services = extract_services(nmap_raw_output) 
    search_exploits(services, f"reports/exploits_{timestamp}.txt")

    # DeepSeek analizi
    print("\n--- DeepSeek Analizi ---")
    # analyze_with_deepseek fonksiyonunun artık analiz metnini döndürdüğünü varsayıyoruz.
    deepseek_report_content = analyze_with_deepseek(
        args.api_key,
        nmap_raw_output, # DeepSeek analizi için Nmap ham çıktısını gönderiyoruz
        f"reports/deepseek_analysis_{timestamp}.txt"
    )
    
    if not deepseek_report_content:
        print("[UYARI] DeepSeek analizinden içerik alınamadı veya bir hata oluştu.")
        deepseek_report_content = "DeepSeek analizi yapılamadı veya sonuç alınamadı." # Rapor boş olmasın diye

    ########## RAPOR HEDEF BİLGİLERİ ############
    report_target_info = {
        'ip': args.target,
        'url': target_url if target_url else args.target, # Eğer bir web URL'si tespit edildiyse kullan
        'scan_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    ############## Rapor dönüştürme ###############
    handle_reporting(
        report_target_info, 
        nmap_raw_output,         # Ham Nmap çıktısı gönderildi
        deepseek_report_content, # DeepSeek analiz metni gönderildi
        f"pentest_report_{timestamp}"
    )
    # ----------------------------------------

    print("\n--- Tarama ve Raporlama tamamlandı! ---")
        
if __name__ == "__main__":
    check_all_dependencies()
    main()