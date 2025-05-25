# scanner.py

import subprocess
import os
from utils import extract_open_ports

def run_nmap(command, timeout=300):
    try:
        print(f"[BİLGİ] Nmap komutu çalıştırılıyor: {' '.join(command)}")
        result = subprocess.run(command, text=True, capture_output=True, timeout=timeout)
        return result.stdout
    except subprocess.TimeoutExpired:
        print("[HATA] Nmap komutu zaman aşımına uğradı!")
        return None
    except Exception as e:
        print(f"[HATA] Nmap çalıştırılamadı: {e}")
        return None

def perform_full_scan(target, output_file):
    combined_results = []

    print("[BİLGİ] Firewall kontrolü yapılıyor...")
    firewall_result = run_nmap(["nmap", "-Pn", "-p", "80", "--script", "http-waf-detect", target])
    firewall_detected = firewall_result and "is behind a firewall" in firewall_result

    if firewall_detected:
        print("[BİLGİ] Firewall bulundu. Stealth tarama yapılıyor...")
        scan_result = run_nmap([
            "nmap", "-sS", "-T2", "-A",
            "--data-length", "20",
            "--randomize-hosts",
            "--badsum", target
        ])
    else:
        print("[BİLGİ] Firewall bulunamadı. Agresif tarama yapılıyor...")
        scan_result = run_nmap(["nmap", "-A", "-T4", target])

    vuln_scan_result = run_nmap(["nmap", "--script", "vuln", target])

    combined_results.append(firewall_result)
    combined_results.append(scan_result)
    combined_results.append(vuln_scan_result)

    full_output = "\n".join(filter(None, combined_results))

    os.makedirs("reports", exist_ok=True)
    with open(output_file, "w") as file:
        file.write(full_output)

    print(f"[BİLGİ] Taramalar {output_file} dosyasına kaydedildi.")

    open_ports = extract_open_ports(scan_result)
    return firewall_detected, open_ports, full_output

def subnet_discovery(subnet, output_file):
    print(f"[BİLGİ] Subnet ({subnet}) üzerinde ağ keşfi yapılıyor...")
    result = run_nmap(["nmap", "-sn", subnet])

    if result:
        with open(output_file, "w") as file:
            file.write(result)
        print(f"[BİLGİ] Subnet tarama sonuçları {output_file} dosyasına kaydedildi.")
    else:
        print("[HATA] Subnet taraması başarısız oldu.")
