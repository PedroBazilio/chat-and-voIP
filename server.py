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
        list()


def handle_client(client):  # Leva socket do cliente como argumento.
    """Lida com uma conexão singular do cliente."""
    
    name = client.recv(BUFSIZ).decode("utf8")
    print("O nome do usuário é ", name)
    vrf = vrfName(name,client)
    while vrf != True:
        client.send(bytes("Digite outro nome: ", "utf8"))
        vrf = vrfName(name,client)
    
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
            listUsr(nome_decodeVar)
        else:

            if msg == lista1:
                list()

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



def list():
    
    for cli, addr in zip(clients, addresses):
        lista = (f'|Nome: {clients[cli]} | IP & Porta: {addresses[addr]} |\n')
        #print(lista.encode('ascii'))
        broadcast(lista.encode('ascii'))



def listUsr(name):
    
    for cli, addr in zip(clients, addresses):
        if name == clients[cli]:
            msg = (f'| IP & Porta de {name} : {addresses[addr]} |')
            broadcast(msg.encode('ascii'))
            #cli.send(bytes(msg, 'utf8'))
        
    broadcast(bytes("Usuario não encontrado.", "utf8"))
    


def decodeVar(var):
    seq = var.decode()
    #comp = seq.startswith("Pesquisa")
    return seq.startswith("Pesquisa")
    

def vrfName(varNome, client):
    for nome in clients:
        if varNome == clients[nome]:
            client.send(bytes("Usuário já existe", "utf8"))
            # broadcast(bytes("Usuario já existe.", "utf8"))
            name = client.recv(BUFSIZ).decode("utf8")
            return False
            
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
