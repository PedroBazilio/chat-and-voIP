"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread



def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()
        list()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    
    name = client.recv(BUFSIZ).decode("utf8")
    
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    
    while True:
        msg = client.recv(BUFSIZ)

        out = '{quit}'
        quit = bytes(out, 'utf-8')

        lista = 'list'
        lista1 = bytes(lista, 'utf-8')
        
        search = transf(msg)
        if search == True:

            tamMsg = len(msg)
            slice_obj = slice(9, tamMsg)
            Name = msg[slice_obj]
            nome_transf = str(Name, 'utf-8')
            listUsr(nome_transf)
        else:

            if msg == lista1:
                list()

            elif msg != quit:
                broadcast(msg, name+": ")
            
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                broadcast(bytes("%s has left the chat." % name, "utf8"))
                break
   



def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)



def list():
    
    for cli, addr in zip(clients, addresses):
        lista = (f'|Nome: {clients[cli]} | IP & Porta: {addresses[addr]} |')
        print(lista.encode('ascii'))
        #broadcast(lista.encode('ascii'))



def listUsr(name):
    
    for cli, addr in zip(clients, addresses):
        if name == clients[cli]:
            msg = (f'| IP & Porta de {name} : {addresses[addr]} |')
            #broadcast(msg.encode('ascii'))
            cli.send(bytes(msg, 'utf8'))
        
    broadcast(bytes("Usuario não encontrado.", "utf8"))
    


def transf(var):
    seq = var.decode()
    comp = seq.startswith("Pesquisa")
    return comp 
    




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
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()