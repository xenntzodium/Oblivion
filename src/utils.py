# utils.py

import ipaddress
import re
import socket

def validate_ip_or_subnet(target):
    # IP v4 regex
    ipv4_regex = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    # Subnet regex (CIDR)
    subnet_regex = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(?:[0-9]|[1-2][0-9]|3[0-2])$"

    # 1. IP veya Subnet kontrolü
    if re.match(ipv4_regex, target):
        return True
    if re.match(subnet_regex, target):
        return True

    # 2. Domain/Hostname kontrolü
    # Basit bir domain kontrolü yapalım ve sonra çözmeye çalışalım
    if "." in target and not target.startswith("http"): # http/https ile başlamıyorsa ve . içeriyorsa domain olabilir
        try:
            # Hostname'i IP adresine çözmeye çalış
            socket.gethostbyname(target)
            return True # Çözülebiliyorsa geçerli bir domaindir
        except socket.gaierror:
            # Çözülemezse geçersiz domaindir
            return False
        except Exception as e:
            print(f"[HATA] Domain doğrulama sırasında beklenmeyen hata: {e}")
            return False

    return False # Hiçbir formata uymuyorsa geçersiz

def extract_open_ports(nmap_output):
    """
    Nmap çıktısından açık portları listeler.
    """
    open_ports = []
    for line in nmap_output.splitlines():
        if "/tcp" in line and "open" in line:
            port = int(line.split("/")[0])
            open_ports.append(port)
    return open_ports

def extract_services(nmap_output):
    """
    Nmap çıktısından servis isimlerini döndürür.
    """
    services = []
    for line in nmap_output.splitlines():
        if "/tcp" in line and "open" in line:
            parts = line.split()
            if len(parts) >= 3:
                services.append(parts[2])
    return services
