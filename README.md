# Oblivion
Automated Penetration Testing Tool

Bu aracın temel amacı, pentest hakkında hiçbir bilgisi olmayan birinin bile temel seviyede bir pentest yapabilmesini sağlamaktır. Kullanıcı, bu sayede raporda sistemlerinde bulunan açıkları anlayıp, AI desteğiyle önerilen çözümleri uygulayarak bu açıkları kapatabilir.

Oblivion Framework
Oblivion Framework, hedef IP, domain veya subnet üzerinde tamamen otomatik çalışan, modüler bir sızma testi aracıdır. Hızlı keşif, güvenlik açığı analizi, web uygulama taraması, SQL Injection testi ve Exploit-DB üzerinden exploit araştırması gibi işlemleri tam otomatik olarak gerçekleştirir.

🚀 Özellikler
  🔎 Ağ Keşfi ve Cihaz Analizi: Belirtilen subnet üzerinde aktif cihaz taraması yapar.

  🛡️ Firewall Algılama: Hedef üzerinde güvenlik duvarı tespiti ve dinamik tarama adaptasyonu sağlar.

  ⚡ Port ve Servis Tespiti: Detaylı Nmap taramaları (OS Detection, Service Enumeration, Vulnerability Scripts).

  🕵️ SQL Injection Taraması: Web portları (80, 443, 8080) açık olan hedeflerde otomatik SQLmap taraması yapar.

  🗂️ Web Dizini Taraması: Web sunucuları için Gobuster kullanarak dizin keşfi gerçekleştirir.

  🔥 Exploit Araması: Açık servisler için Exploit-DB veritabanı üzerinden exploit araştırması (searchsploit) yapar.

  🤖 AI Destekli Raporlama: DeepSeek API kullanılarak detaylı ve profesyonel pentest raporu oluşturulur.

  📂 Tam Dosya Yönetimi: Tüm tarama ve analiz çıktıları reports/ klasörüne otomatik olarak kaydedilir.

  🛠️ Kullanıcı Dostu CLI: Sadece 2 zorunlu, 1 opsiyonel parametre ile çalışır.( 1 zorunlu, 2 opsiyonel olarak düzeltilecek )


  📦 Modüler Yapı
    Oblivion/
  ├── main.py             # Ana kontrol akışı
  ├── utils.py            # Yardımcı fonksiyonlar (doğrulama, port/servis ayıklama)
  ├── scanner.py          # Nmap taramaları + Subnet keşfi
  ├── sqlscanner.py       # SQL Injection taraması (SQLmap)
  ├── dirscanner.py       # Web dizini taraması (Gobuster)
  ├── analyzer.py         # DeepSeek API ile analiz ve raporlama
  ├── exploitscanner.py   # Exploit-DB araştırması (searchsploit)
  └── reports/            # Tüm tarama sonuçlarının kaydedildiği klasör
          Her modül bağımsız çalışır ve kolayca genişletilebilir.

🧰 Kurulum
  Gerekli Python Kütüphaneleri:
    pip install requests


Harici Araçlar:
  Aşağıdaki araçların sisteminizde kurulu olması gerekir:

    Araç	                         Kurulum Komutu
    nmap	                  sudo apt install nmap
    sqlmap	                sudo apt install sqlmap veya SQLmap resmi repo
    gobuster	              sudo apt install gobuster veya go install github.com/OJ/gobuster/v3@latest
    searchsploit	          sudo apt install exploitdb

⚙️ Kullanım
  Temel Komut:
    python3 main.py --target <HEDEF_IP/DOMAIN> --api_key <API_KEY> [--subnet <SUBNET>]

  Örnek Kullanım:
  
    Tek hedef taraması:
      python3 main.py --target 192.168.1.10 --api_key sk-xxxxxxx
      
    Subnet taramasıyla birlikte:
      python3 main.py --target 192.168.1.10 --subnet 192.168.1.0/24 --api_key sk-xxxxxxx

🛡️ Yetenekler Listesi

  Yetenek	Açıklama
    Firewall Detection:	HTTP WAF tespiti ve adaptif tarama
    Port Scanning:	Hızlı ve detaylı TCP port taraması
    OS/Service Detection:	İşletim Sistemi ve Servis versiyonlarını algılar
    Vulnerability Scripts:	Nmap Vuln Scriptleri ile zaafiyet taraması
    SQL Injection Testing:	Web tabanlı hedeflerde otomatik SQLmap taraması
    Directory Bruteforce:	Gobuster ile dizin keşfi
    Exploit Lookup:	Servis bazlı Exploit-DB araştırması
    AI Report:	DeepSeek kullanılarak profesyonel zafiyet raporu oluşturulması


🧠 Neden Oblivion Framework?

Zaman Kazandırır: Tek komutla ağ keşfi, zafiyet analizi ve raporlama.
Tam Otomatik: Kullanıcıdan müdahale istemez.
Modüler: İstediğiniz zaman kendi modüllerinizi kolayca ekleyebilirsiniz.
Gerçek Dünya Pentestlerine Uygundur: Profesyonel sızma testi senaryolarını simüle eder.


⚠️ Yasal Uyarı
Bu araç sadece izinli hedeflerde kullanılmalıdır. Yetkisiz sistemlere yapılan taramalar ve saldırılar yasadışıdır. Kullanıcı, aracın kullanımından doğacak tüm yasal sorumlulukları üstlenmektedir.


👨‍💻 Geliştirici
Proje Sahibi: zorbeyyavas






  
