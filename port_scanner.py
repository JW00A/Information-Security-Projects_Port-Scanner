import socket
import ipaddress
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose = False):
    open_ports = []

    try:
        ipaddress.ip_address(target)
        is_ip = True
    except ValueError:
        is_ip = False

    try:
        if is_ip:
            ip = target
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except socket.herror:
                hostname = None
        else:
            hostname = target
            ip = socket.gethostbyname(target)

        for port in range(min(port_range), max(port_range) + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0)
                result = s.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
        
        if verbose:
            display_name = hostname if hostname else ip
            if display_name != ip:
                out = f'Open ports for {display_name} ({ip})\nPORT     SERVICE'
            else:
                out = f'Open ports for {display_name}\nPORT     SERVICE'
            
            for port in open_ports:
                out += f'\n{str(port).ljust(9)}{ports_and_services[port]}'
            return out
        else:
            return open_ports
    except socket.gaierror:
        if is_ip or target.replace('.', '').isdigit():
            return 'Error: Invalid IP address'
        else:
            return 'Error: Invalid hostname'