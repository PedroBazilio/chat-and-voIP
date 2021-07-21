from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


#pegando o hostname
hostname = socket.gethostname()

#pegando o ip
ip_address = socket.gethostbyname(hostname)


print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")