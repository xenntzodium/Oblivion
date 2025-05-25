import shutil
import importlib.util
import subprocess
import sys

required_tools = ["nmap", "sqlmap", "gobuster", "searchsploit"]
required_python_modules = ["requests", "Crypto"]

def check_tool_installed(tool):
    return shutil.which(tool) is not None

def check_module_installed(module_name):
    return importlib.util.find_spec(module_name) is not None

def prompt_and_install_tool(tool):
    print(f"[!] Gerekli araç yüklü değil: {tool}")
    user_input = input(f"[?] {tool} aracını yüklemek ister misiniz? [y/N]: ").strip().lower()
    if user_input == 'y':
        try:
            subprocess.run(["sudo", "apt", "install", "-y", tool], check=True)
            print(f"[+] {tool} başarıyla yüklendi.")
        except subprocess.CalledProcessError:
            print(f"[HATA] {tool} yüklenemedi!")
    else:
        print(f"[!] {tool} yüklenmeden devam ediliyor.")

def prompt_and_install_module(module_name, pip_name=None):
    pip_package = pip_name if pip_name else module_name
    print(f"[!] Python modülü eksik: {module_name}")
    user_input = input(f"[?] {pip_package} modülünü yüklemek ister misiniz? [y/N]: ").strip().lower()
    if user_input == 'y':
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", pip_package], check=True)
            print(f"[+] {pip_package} başarıyla yüklendi.")
        except subprocess.CalledProcessError:
            print(f"[HATA] {pip_package} yüklenemedi!")
    else:
        print(f"[!] {pip_package} yüklenmeden devam ediliyor.")

def check_all_dependencies():
    print("[BİLGİ] Sistem bağımlılıkları kontrol ediliyor...")

    for tool in required_tools:
        if not check_tool_installed(tool):
            prompt_and_install_tool(tool)
        else:
            print(f"[✓] {tool} yüklü.")

    for module in required_python_modules:
        if not check_module_installed(module):
            # PyCryptodome modülü 'Crypto' adını kullanır
            pip_pkg = "pycryptodome" if module == "Crypto" else module
            prompt_and_install_module(module, pip_pkg)
        else:
            print(f"[✓] Python modülü {module} yüklü.")

    print("[BİLGİ] Tüm kontroller tamamlandı.")
