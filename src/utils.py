# utils.py

import ipaddress

def validate_ip_or_subnet(target):
    """
    IP veya subnet doğrulaması yapar.
    """
    try:
        ipaddress.ip_network(target, strict=False)
        return True
    except ValueError:
        return False

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
