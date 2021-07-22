from os import truncate
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

#aceitando conexões
#composto por um loop que espera infinitamente por conexões que cheguem
#e assim que as recebe imprime na tela detalhes da conexão e envia uma mensagem de boas vindas
#também aramazena o endereço do cliente na biblioteca "adresses" em depois
#por final iniciando uma thread para esse cliente
def accept_incoming_connections():
    while True:
        client, client_adresses = SERVER.accept()
        print("%s:%s conectou-se." % client_adresses)
        client.send(bytes("Olá estranho!!!"+
                            "Digite o seu nome e pressione enter",
        "utf8"))
        adresses[client] = client_adresses
        print (adresses[client])
        Thread(target=handle_client, args=(client,)).start()



def handle_client(client): #recebe um socket como argumento
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = "Bem vindo(a) %s!!! Se deseja sair, digite {quit}." %name
    client.send(bytes(welcome, "utf8"))
    msg = "%s entrou no chat" %name
    broadcast = (bytes(msg, "utf8"))
    clients[client] = name
    while True:
        #envio da lista de nomes vai aqui
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            #del clients[client]
            #broadcast(bytes("%s saiu do chat." %name, "utf8"))
            break


def broadcast(msg, prefix=""): #prefixo é para a identificação do nome
    #mensagem broadcast para todos os clientes
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+ msg)


clients = {}
adresses = {}
IPs = {}
HOST = ''
PORT = 5000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


if __name__ == "__main__":
    SERVER.listen(5) #aceita no maximo 5 conexões
    print("Aguardando conexão...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()




# #pegando o hostname

# hostname = socket.gethostname()

# #pegando o ip
# ip_address = socket.gethostbyname(hostname)


# print(f"Hostname: {hostname}")
# print(f"IP Address: {ip_address}")

