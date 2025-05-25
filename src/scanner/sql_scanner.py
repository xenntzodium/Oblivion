# sqlscanner.py

import subprocess

def run_sqlmap(target, firewall_detected, output_file):
    print(f"[BİLGİ] SQLMap taraması başlatılıyor: {target}")

    if firewall_detected:
        sqlmap_command = [
            "sqlmap", "-u", target,
            "--tamper=between,randomcase",
            "--random-agent",
            "--timeout=10",
            "--retries=2",
            "--batch",
            "--risk=1",
            "--level=1"
        ]
    else:
        sqlmap_command = [
            "sqlmap", "-u", target,
            "--batch",
            "--risk=3",
            "--level=5",
            "--threads=5"
        ]

    try:
        result = subprocess.run(sqlmap_command, capture_output=True, text=True)
        with open(output_file, "w") as file:
            file.write(result.stdout)
        print(f"[BİLGİ] SQLMap sonuçları {output_file} dosyasına kaydedildi.")
    except Exception as e:
        print(f"[HATA] SQLMap çalıştırılamadı: {e}")
