import socket

#pegando o hostname
hostname = socket.gethostname()

#pegando o ip
ip_address = socket.gethostbyname(hostname)


print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")