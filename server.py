from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

enderecos = {}
lista_usuarios = {}

def tratamento_nome_e_mensagem(cliente):  # Leva socket do clientee como argumento.    
    name = cliente.recv(TAM_BUFFER).decode("utf8")
    vrf = vrfName(name,cliente)
    while vrf != True:
        cliente.send(bytes("Digite outro nome: ", "utf8"))
        name = cliente.recv(TAM_BUFFER).decode("utf8")
        vrf = vrfName(name,cliente)
    vrf = False
    while True:
        mensagem = cliente.recv(TAM_BUFFER)
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
            listUsr(nome_decodeVar, cliente)
        else:

            if mensagem == lista1:
                list(cliente)

            elif mensagem != quit:
                for sock in lista_usuarios:
                    sock.send(bytes(name+": ", "utf8")+mensagem)
            
            else:
                cliente.send(bytes("{sair}", "utf8"))
                cliente.close()
                del lista_usuarios[cliente]
                for sock in lista_usuarios:
                    sock.send(bytes(name+" Saiu." , "utf8"))
                break   

def list(cliente):   
    for cli, addr in zip(lista_usuarios, enderecos):
        lista = (f'|Nome: {lista_usuarios[cli]} | IP & Porta: {enderecos[addr]} |\n')
        #print(lista.encode('ascii'))
        cliente.send(lista.encode('ascii'))



def listUsr(name, cliente):
    for cli, addr in zip(lista_usuarios, enderecos):
        if name == lista_usuarios[cli]:
            msg = (f'| IP & Porta de {name} : {enderecos[addr]} |')
            cliente.send(msg.encode('ascii'))
            return
            
        
    cliente.send(bytes("Usuario não encontrado.", "utf8"))
    

def decodeVar(var):
    seq = var.decode()
    return seq.startswith("Pesquisa")


def vrfName(varNome, cliente):
    for nome in lista_usuarios:
        if varNome == lista_usuarios[nome]:
            cliente.send(bytes("Usuário já existe", "utf8"))
            return False
    print("O nome do usuário é ", varNome)      
    cliente.send(bytes(('Usuário %s cadastrado.' % varNome), "utf8"))
    cliente.send(bytes(('Se desejar sair, digite {sair}.'), "utf8"))
    for sock in lista_usuarios:
        sock.send(bytes(varNome+" Entrou!" , "utf8"))
    lista_usuarios[cliente] = varNome
    return True

def conectar_ao_usuario():
    while True:
        cliente, cliente_address = SERVER.accept()
        print("%s|%s entrou" % cliente_address)
        cliente.send(bytes("Digite seu nome", "utf8"))
        enderecos[cliente] = cliente_address
        Thread(target=tratamento_nome_e_mensagem, args=(cliente,)).start()
        list(cliente)



TAM_BUFFER = 1024
HOST = ''
PORT = 5000
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
SERVER.listen(5)
print("Aguardando Conexão...")
RECEBE_THREAD = Thread(target=conectar_ao_usuario)
RECEBE_THREAD.start()
RECEBE_THREAD.join()
SERVER.close()