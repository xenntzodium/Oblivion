# dirscanner.py

import subprocess

def run_gobuster(target, wordlist, output_file):
    print(f"[BİLGİ] Gobuster taraması başlatılıyor: {target}")

    gobuster_command = [
        "gobuster", "dir",
        "-u", target,
        "-w", wordlist,
        "-t", "50",
        "-o", output_file,
        "--timeout", "10s"
    ]

    try:
        subprocess.run(gobuster_command, check=True)
        print(f"[BİLGİ] Gobuster sonuçları {output_file} dosyasına kaydedildi.")
    except Exception as e:
        print(f"[HATA] Gobuster çalıştırılamadı: {e}")
