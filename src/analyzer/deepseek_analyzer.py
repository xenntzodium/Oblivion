# src/analyzer/deepseek_analyzer.py
import requests

def analyze_with_deepseek(api_key, combined_results, output_file):
    try:
        print("[BİLGİ] DeepSeek analizi başlatılıyor...")
        
        # DeepSeek API'sinin güncel URL'si ve model adı (Dokümantasyondan teyit ediniz)
        url = "https://api.deepseek.com/chat/completions" 
        # DeepSeek'in sunduğu modeller: deepseek-chat, deepseek-coder (varsayılan olarak deepseek-coder kullandım)
        model_name = "deepseek-coder" 

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": "You are a cybersecurity assistant analyzing Nmap scan results and other pentest data. Provide actionable insights and potential vulnerabilities."},
                {"role": "user", "content": f"Analyze the following pentest results and provide a detailed report including identified services, potential vulnerabilities, and recommendations:\n\n{combined_results}"}
            ],
            "stream": False # Streaming'i kapatıp tam yanıt alalım
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status() # HTTP hataları için istisna fırlat

        response_data = response.json()
        analysis = response_data["choices"][0]["message"]["content"]
        
        with open(output_file, "w", encoding="utf-8") as file: # Encoding eklendi
            file.write(analysis)
        print(f"[BİLGİ] DeepSeek raporu {output_file} dosyasına kaydedildi.")
        
        return analysis # Analiz metnini döndür
    except requests.exceptions.RequestException as e:
        print(f"[HATA] DeepSeek API bağlantı hatası: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"API Yanıtı (Hata): {e.response.text}")
        return ""
    except (KeyError, IndexError):
        print("[HATA] DeepSeek API yanıt formatı beklenenden farklı. 'choices' veya 'message' bulunamadı.")
        return ""
    except Exception as e:
        print(f"[HATA] DeepSeek analizi sırasında beklenmeyen hata: {e}")
        return ""