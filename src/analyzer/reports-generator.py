# reports/report_generator.py
import os
import subprocess
import datetime

def generate_markdown_report(target_info, nmap_results, whatweb_results, filename_prefix="pentest_report"):
    """
    Tarama sonuçlarını içeren basit bir Markdown raporu oluşturur.
    ... (Daha önceki generate_markdown_report fonksiyonunun içeriği aynı kalacak) ...
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    target_info['scan_time'] = current_time

    report_content = f"# Otomatize Pentest Raporu - {target_info.get('url', target_info.get('ip', 'Bilinmeyen Hedef'))}\n\n"
    report_content += f"**Tarama Zamanı:** {target_info.get('scan_time', 'N/A')}\n"
    report_content += f"**Hedef:** {target_info.get('url', 'N/A')} ({target_info.get('ip', 'N/A')})\n\n"

    report_content += "## 1. Nmap Tarama Sonuçları\n"
    if nmap_results:
        report_content += "| Port | Servis |\n"
        report_content += "|---|---|\n"
        for result in nmap_results:
            report_content += f"| {result['port']} | {result['service']} |\n"
    else:
        report_content += "Nmap taramasında açık port bulunamadı veya sonuç alınamadı.\n"
    report_content += "\n"

    report_content += "## 2. WhatWeb Analiz Sonuçları\n"
    if whatweb_results:
        for tech in whatweb_results:
            report_content += f"- {tech}\n"
    else:
        report_content += "WhatWeb analizinde teknoloji bilgisi bulunamadı.\n"
    report_content += "\n"

    report_content += "## 3. Ek Notlar\n"
    report_content += "Bu rapor, otomatik pentest aracı tarafından oluşturulmuştur. Daha detaylı analizler gerekebilir.\n"

    markdown_filepath = os.path.join("reports", f"{filename_prefix}.md")

    try:
        with open(markdown_filepath, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"✅ Markdown raporu başarıyla oluşturuldu: {markdown_filepath}")
        return markdown_filepath
    except IOError as e:
        print(f"❌ Markdown raporu oluşturulurken bir hata oluştu: {e}")
        return None

def convert_report_with_pandoc(markdown_filepath, output_format="pdf", output_filename=None):
    """
    Pandoc kullanarak Markdown raporunu belirtilen formata dönüştürür.
    ... (Daha önceki convert_report_with_pandoc fonksiyonunun içeriği aynı kalacak) ...
    """
    if not markdown_filepath or not os.path.exists(markdown_filepath):
        print(f"❌ Hata: Markdown dosyası bulunamadı: {markdown_filepath}")
        return None

    if output_filename is None:
        base_name = os.path.splitext(os.path.basename(markdown_filepath))[0]
        output_filename = f"{base_name}.{output_format}"
    
    output_filepath = os.path.join("reports", output_filename)
    
    if output_format == 'pdf':
        command = ['pandoc', markdown_filepath, '-o', output_filepath, '--pdf-engine=pdflatex']
    else:
        command = ['pandoc', markdown_filepath, '-o', output_filepath]

    print(f"🔄 Rapor {output_format} formatına dönüştürülüyor: {output_filepath}")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"✅ Rapor başarıyla {output_format} formatına dönüştürüldü: {output_filepath}")
        if result.stdout:
            print("Pandoc çıktısı (stdout):\n", result.stdout)
        if result.stderr:
            print("Pandoc hataları/uyarıları (stderr):\n", result.stderr)
        return output_filepath
    except FileNotFoundError:
        print(f"❌ Hata: Pandoc bulunamadı. Lütfen sisteminizde Pandoc'un yüklü ve PATH'inizde olduğundan emin olun.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"❌ Hata: Pandoc dönüşüm sırasında bir hata oluştu: {e}")
        print("Pandoc komutu:", " ".join(command))
        print("Pandoc çıktısı (stdout):\n", e.stdout)
        print("Pandoc hataları (stderr):\n", e.stderr)
        return None
    except Exception as e:
        print(f"❌ Beklenmeyen bir hata oluştu: {e}")
        return None

# `if __name__ == "__main__":` bloğunu kaldırıyoruz veya yorum satırı yapıyoruz.
# Çünkü bu dosya artık bir modül olarak içe aktarılacak, kendi başına çalışmayacak.
# Bu test bloğu main.py'de yer alacak.