# analyzer.py

import requests

def analyze_with_deepseek(api_key, combined_results, output_file):
    try:
        print("[BİLGİ] DeepSeek analizi başlatılıyor...")
        url = ""
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "",
            "messages": [
                {"role": "system", "content": "You are a cybersecurity assistant analyzing Nmap scan results."},
                {"role": "user", "content": f"Analyze the following Nmap scan results and provide a detailed report:\n\n{combined_results}"}
            ]
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            analysis = response_data["choices"][0]["message"]["content"]
            with open(output_file, "w") as file:
                file.write(analysis)
            print(f"[BİLGİ] DeepSeek raporu {output_file} dosyasına kaydedildi.")
        else:
            print(f"[HATA] DeepSeek API hatası: {response.status_code}")
    except Exception as e:
        print(f"[HATA] DeepSeek bağlantı hatası: {e}")
