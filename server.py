"""Server para aplicação de chat assíncrona."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread



def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s se conectou." % client_address)
        client.send(bytes("Bem vindo ao nosso local! Digite seu nome e pressione enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()
        list(client)


def handle_client(client):  # Leva socket do cliente como argumento.
    """Lida com uma conexão singular do cliente."""
    
    name = client.recv(BUFSIZ).decode("utf8")
    vrf = vrfName(name,client)
    while vrf != True:
        vrfName(name, client)
    # welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    # client.send(bytes(welcome, "utf8"))
    # msg = "%s has joined the chat!" % name
    # broadcast(bytes(msg, "utf8"))
    # clients[client] = name
    
    while True:
        msg = client.recv(BUFSIZ)

        out = '{sair}'
        quit = bytes(out, 'utf-8')

        lista = 'list'
        lista1 = bytes(lista, 'utf-8')
        
        search = decodeVar(msg)
        if search == True:

            tamMsg = len(msg)
            slice_obj = slice(9, tamMsg)
            Name = msg[slice_obj]
            nome_decodeVar = str(Name, 'utf-8')
            listUsr(nome_decodeVar, client)
        else:

            if msg == lista1:
                list(client)

            elif msg != quit:
                broadcast(msg, name+": ")
            
            else:
                client.send(bytes("{sair}", "utf8"))
                client.close()
                del clients[client]
                broadcast(bytes("%s has left the chat." % name, "utf8"))
                break
   



def broadcast(msg, prefix=""):  # prefixo é para identificação do nome.
    """Envia uma mensagem em broadcast para todos os clientes."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)



def list(client):
    
    for cli, addr in zip(clients, addresses):
        lista = (f'|Nome: {clients[cli]} | IP & Porta: {addresses[addr]} |\n')
        #print(lista.encode('ascii'))
        client.send(lista.encode('ascii'))



def listUsr(name, client):
    
    for cli, addr in zip(clients, addresses):
        if name == clients[cli]:
            msg = (f'| IP & Porta de {name} : {addresses[addr]} |')
            client.send(msg.encode('ascii'))
            
        
    client.send(bytes("Usuario não encontrado.", "utf8"))
    


def decodeVar(var):
    seq = var.decode()
    #comp = seq.startswith("Pesquisa")
    return seq.startswith("Pesquisa")
    

def vrfName(varNome, client):
    for nome in clients:
        if varNome == clients[nome]:
            broadcast(bytes("Usuario inexistente.", "utf8"))
            name = client.recv(BUFSIZ).decode("utf8")
            return False
    
    print('O usuário se chama: ', varNome)
    welcome = 'Bem-Vindo %s! Se desejar sair, digite {sair}.' % varNome
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % varNome 
    broadcast(bytes(msg, "utf8"))
    clients[client] = varNome
    return True

clients = {}
addresses = {}


HOST = ''
PORT = 5000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Aguardando Conexão...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
