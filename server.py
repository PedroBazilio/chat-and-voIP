from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM
from threading import Thread
import pyaudio

enderecos = {}
lista_usuarios = {}

def tratamento_nome_e_mensagem(cliente):  #Recebe o socket do cliente para aceitar tratar as entradas do cliente.    
    name = cliente.recv(TAM_BUFFER).decode("utf8")
    vrf = vrfName(name,cliente)   #chama a função vrfName para adicionar o nome do cliente na lista, retornando false ou true para saber se é necessário chamar a função de novo
    while vrf != True:
        cliente.send(bytes("Digite outro nome: ", "utf8"))
        name = cliente.recv(TAM_BUFFER).decode("utf8")
        vrf = vrfName(name,cliente)
    vrf = False
    while True:
        mensagem = cliente.recv(TAM_BUFFER)   #String escrita pelo usuário
        
        estaNaLista = False
        var_audio = '!@#$%'
        audio = bytes(var_audio, 'utf8')

        out = '{sair}'
        quit = bytes(out, 'utf-8')
        lista = 'list'
        lista1 = bytes(lista, 'utf-8')
        
        search = decodeVar(mensagem) #Verificação se a palavra "Pesquisa" foi escrita

        if mensagem.startswith(audio):
            nome = mensagem[5:]
            nome = nome.decode('utf8')
            for cli, addr_dest in zip(lista_usuarios, enderecos): #procura pelo nome
                if nome == lista_usuarios[cli]:
                    estaNaLista = True
                    break
            if(estaNaLista):
                addr_dest.send(bytes("recebe_ligacao", "utf8"))

        elif mensagem.startswith(bytes("Pesquisa", "utf8")):
            mensagem = mensagem.decode('utf8')
            mensagem = mensagem[9:]
            print(mensagem)
            listUsr(mensagem, cliente) #Chama a função para procurar o usuário
        else:

            if mensagem == lista1:
                list(cliente) #caso o usuário tenha escrito "list" para listar todos os usuários presentes
            elif mensagem == quit: 
                cliente.close()   #Cliente se desliga do servidor e aplicação é fechada
                del lista_usuarios[cliente] #deleta o usuário da lista de usuários
                for sock in lista_usuarios:
                    sock.send(bytes(name+" Saiu." , "utf8"))
                break


            else:
                for sock in lista_usuarios:  #Manda a mensagem escrita pelo usuário para todos e para si mesmo, mostrando o nome de quem mandou
                    sock.send(bytes(name+": ", "utf8")+mensagem)

def list(cliente):   #Recebe o socket do cliente para printar para ele os usuários presentes
    for cli, addr in zip(lista_usuarios, enderecos):   #for por todos os usuários
        lista = (f'\n|Nome: {lista_usuarios[cli]} | IP & Porta: {enderecos[addr]} |\n')
        #print(lista.encode('ascii'))
        cliente.send(lista.encode('ascii'))



def listUsr(name, cliente): #Recebe o nome que está sendo procurado e o socket do cliente que deseja saber
    for cli, addr in zip(lista_usuarios, enderecos): #procura pelo nome
        if name == lista_usuarios[cli]:
            msg = (f'| IP & Porta de {name} : {enderecos[addr]} |')
            cliente.send(msg.encode('ascii')) #Escreve somente para o cliente a mensagem de que o usuário foi encontrado
            return
            
        
    cliente.send(bytes("Usuario não encontrado.", "utf8"))  #Dizendo que o usuário não foi encontrado
    

def decodeVar(var): #Recebe a string do usuário. Caso comece com "Pesquisa" retorna True
    seq = var.decode()
    return seq.startswith("Pesquisa")


def vrfName(varNome, cliente):  #Recebe o nome digitado pelo usuário e o socket do cliente para adiciona-lo na lista
    for nome in lista_usuarios:  #for para saber se o nome já está na lista
        if varNome == lista_usuarios[nome]:
            cliente.send(bytes("Usuário já existe", "utf8"))
            return False   #retorna false se o nome já estiver na lista para que entre no while e saia apenas quando o nome for válido
    
    print("O nome do usuário é ", varNome)      
    cliente.send(bytes(('Usuário %s cadastrado.' % varNome), "utf8"))
    
    for sock in lista_usuarios:  #mostra para todos os usuários o nome da pessoa que entrou
        sock.send(bytes(varNome+" Entrou!" , "utf8"))
    lista_usuarios[cliente] = varNome #adiciona o nome da lista para que não seja aceito repetições
    return True

def conectar_ao_usuario():    #Função para receber o socket do usuário e conecta-lo ao servidor
    while True:
        cliente, cliente_address = SERVER.accept()   #recebe o socket e o endereço do cliente
        print("%s|%s entrou" % cliente_address)
        list(cliente)
        cliente.send(bytes("Digite seu nome\n", "utf8"))
        enderecos[cliente] = cliente_address   #coloca numa lista o endereço do cliente que está entrando
        Thread(target=tratamento_nome_e_mensagem, args=(cliente,)).start()






TAM_BUFFER = 1024
audio_format = pyaudio.paInt16
channels = 1
rate = 20000
PORT_AUDIO = 6000

AUDIO = pyaudio.PyAudio()
recebe_stream = AUDIO.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=TAM_BUFFER)
    


HOST = ''


PORT_AUDIO = 6000
PORT = 5000   #Porta 5000 especificada para uso do servidor


ADDR = (HOST, PORT)
ADDR_AUDIO = (HOST, PORT_AUDIO)

SERVER = socket(AF_INET, SOCK_STREAM)


SERVER.bind(ADDR)
SERVER.listen(5)



print("Aguardando Conexão...")
RECEBE_THREAD = Thread(target=conectar_ao_usuario)
RECEBE_THREAD.start()
RECEBE_THREAD.join()
SERVER.close()
