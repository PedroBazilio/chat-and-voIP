from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def conectar_ao_usuario():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s se conectou." % client_address)
        client.send(bytes("Bem vindo ao nosso local! Digite seu nome e pressione enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=tratamento_nome_e_mensagem, args=(client,)).start()
        list()


def tratamento_nome_e_mensagem(client):  # Leva socket do cliente como argumento.
    
    name = client.recv(BUFSIZ).decode("utf8")
    print("O nome do usuário é ", name)
    vrf = vrfName(name,client)
    while vrf != True:
        client.send(bytes("Digite outro nome: ", "utf8"))
        name = client.recv(BUFSIZ).decode("utf8")
        vrf = vrfName(name,client)
    vrf = False
    while True:
        mensagem = client.recv(BUFSIZ)
        out = '{sair}'
        quit = bytes(out, 'utf-8')

        lista = 'list'
        lista1 = bytes(lista, 'utf-8')
        
        search = decodeVar(mensagem)
        if search == True:

            tamMsg = len(mensagem)
            slice_obj = slice(9, tamMsg)
            Name = mensagem[slice_obj]
            nome_decodeVar = str(Name, 'utf-8')
            listUsr(nome_decodeVar)
        else:

            if mensagem == lista1:
                list()

            elif mensagem != quit:
                broadcast(mensagem, name+": ")
            
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
    print(varNome)
    for nome in clients:
        if varNome == clients[nome]:
            client.send(bytes("Usuário já existe", "utf8"))
            return False
            
    client.send(bytes(('Bem-Vindo %s! Se desejar sair, digite {sair}.' % varNome), "utf8"))
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
    ACCEPT_THREAD = Thread(target=conectar_ao_usuario)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
