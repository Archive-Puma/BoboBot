import socket

common_ports = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    194: "IRC",
    443: "HTTPS",
    3306: "MySQL",
    25565: "Minecraft",
}

def is_port_open(site, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        sock.connect((site,int(port)))
        sock.close()
    except socket.error:
        return False
    return True

def pmap(site, port):
    if is_port_open(site,port):
        return "[{0}] Port {1} is open!".format(site,port)
    else:
        return "[{0}] Port {1} is close...".format(site,port)

def pmap_common(site):
    ports = [int(x) for x in common_ports.keys()]
    ports.sort()
    resp = str()
    for port in ports:
        if is_port_open(site,port):
            resp = resp + "[{0}] Port {1} is open! Commonly used by {2} service.\n".format(site,str(port),common_ports[int(port)])

    if not resp == "":
        return resp
    else:
        return "[{0}] No common open ports".format(site)
