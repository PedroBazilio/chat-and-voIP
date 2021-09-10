
from tkinter import *
from threading import *
from functools import partial
import socket
import tkinter
import pyaudio


count = 0

def audio():    #Local onde serão tratadas as variáveis do áudio e é chamada a Thread para que seja contínuo

    audio_format = pyaudio.paInt16
    channels = 1
    rate = 20000
 
    AUDIO = pyaudio.PyAudio()
    recebe_stream = AUDIO.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=TAM_BUFFER)
    envia_stream = AUDIO.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=TAM_BUFFER)
    
    recebe_thread = Thread(target=recebe_voz, args=(recebe_stream, socket_audio,))
    transmite_thread = Thread(target=envia_voz, args=(socket_audio, envia_stream,))

    recebe_thread.start()
    transmite_thread.start()


def recebe_voz(recebe_dado, socket):   #Função para receber o áudio
   
    while True:
        try:
            
            data, servidor = socket.recvfrom(TAM_BUFFER * 4)
            print(data)
            recebe_dado.write(data)
        except:
            pass


def envia_voz(socket, manda_dado):   #Função para realizar o envio de voz
    while True:
        try:
            
            data = manda_dado.read(TAM_BUFFER)
            #print(data)
            socket.send(data)

        except:
            pass


def aceitar_chamada(janela):   #Conecta caso seja aceita a chamada
    socket_audio.connect((HOST, PORT_AUDIO))
    janela.destroy()
    audio()

def recusar_chamada(janela):   #Recusa a chamada
    janela.destroy()
    socket_do_cliente.send(bytes("Chamada recusada", "utf8"))



def controle_chamada():    #Função onde fica localizado os botões no popup para controle da chama
    janela_aceita = tkinter.Toplevel()
    janela_aceita.wm_title("Recebendo chamada")
    botao_aceitar = Button(janela_aceita, text="Aceitar", command=lambda: aceitar_chamada(janela_aceita))
    botao_aceitar.pack()

    botao_recursar = Button(janela_aceita, text="Recusar", command= lambda: recusar_chamada(janela_aceita))
    botao_recursar.pack()


def envia_string(janela):      #Adiciona a string !@#$% na string do nome para realizar o controle no servidor
    msg = "!@#$%" + mensagem2.get()
    mensagem2.set("")
    # janela.destroy()
    socket_do_cliente.send(bytes(msg, "utf8"))


def conectar_remetente():  #Chama a função audio por parte do remetente, para realizar a ligação
    print('conectei')
    audio()


def liga(event=None):
    if(count == 0):
        janela_ligacao = tkinter.Toplevel()
        janela_ligacao.wm_title("Ligar")

        nomePesquisa = Entry(janela_ligacao, textvariable=mensagem2)    #Variável que receberá o nome que participará da ligação
        nomePesquisa.bind("<Return>", envia_string) 
        nomePesquisa.pack(side=LEFT, expand=True)
        
        
        botao_nome = Button(janela_ligacao, text="Ligar", command=lambda:envia_string(janela_ligacao))   #Chama a função envia_string para mandar o nome para o servidor
        botao_nome.pack()
        socket_audio.bind(('', PORT_AUDIO))    #Ocorre um bind na porta 6000 por parte de um cliente
        Thread(target=conectar_remetente).start()
        
        

    else:
        janela_no_name = tkinter.Toplevel()
        janela_no_name.geometry("200x20")
        janela_no_name.wm_title()
        text = Label(janela_no_name, text='Você não digitou seu nome ainda!!!')
        text.pack()
        # mensagem_no_name = 'Você não digitou seu nome ainda!!!'

    # socket_do_cliente.send(bytes('!@#$%'))


def fecha_tela(event=None):  #Fecha a tela pelo X, fazendo o mesmo processo de quando se escreve {sair}
    
    mensagem.set("{sair}")
    enviar_msg()

def recebe():    #Recebe a mensagem do server já tratada
    while True:
        try:
            msg = socket_do_cliente.recv(TAM_BUFFER).decode("utf8")
            if(msg == "recebe_ligacao"):   #Se possui a string "recebe_ligacao" na mensagem é chamada a controle_chamada para iniciar a ligação
                resposta = controle_chamada()
            else:
                lista_de_mensagens.insert(END, msg)  #Adiciona a mensagem na tela de mensagens do usuário
        except OSError:
            break

    

def enviar_msg(event=None):  #Enviar a mensagem para o server para ser tratada
    count = 1
    msg = mensagem.get()
    mensagem.set("")
    socket_do_cliente.send(bytes(msg, "utf8"))
    if msg == "{sair}":     #Caso a mensagem escrita, pelo cliente e já tratada pelo servidor, seja {sair} o tkinter é fechado 
        socket_do_cliente.close()
        tk.quit()

def enviar_nome(janela):    #Envia o nome a ser pesquisa para o servidor, adicionando a palavra "Pesquisa"
    msg = "Pesquisa " + mensagem2.get()
    mensagem2.set("")
    janela.destroy()
    socket_do_cliente.send(bytes(msg, "utf8"))



def func_pesquisa():   #Ao clicar no botão pesquisa será aberto essa função, abrindo um popup. E envia para o nome para a função enviar_nome
    janela_pesquisa = tkinter.Toplevel()     
    janela_pesquisa.wm_title("Pesquisa") 
    entrada_nome = Entry(janela_pesquisa, textvariable=mensagem2)

    entrada_nome.bind("<Return>", enviar_nome)    
    entrada_nome.pack()
    botao_nome = Button(janela_pesquisa, text="Pesquisar", command=lambda:enviar_nome(janela_pesquisa))
    botao_nome.pack()

def sair():
    socket_do_cliente.send(bytes("{sair}", "utf8"))   #Manda para o servidor o comando {sair} para o cliente ser excluído da lista no servidor
    socket_do_cliente.close()    #fecha o socket TCP
    tk.quit()  #Fecha a janela do TKinter


tk = Tk()
tk.title("Chat")
frame = Frame()  #Cria um frame

scrollbar = Scrollbar(frame)   #Cria uma scrollbar 
scrollbar.pack(side=RIGHT, fill=Y)   #aAdiciona ela na tela do lado direito preenchendo todo o eixo Y


mensagem = StringVar()    #Variável para receber o valor escrito pelo usuário
mensagem.set("")

mensagem2 = StringVar()    #Variável para receber o valor escrito pelo usuário
mensagem2.set("")

lista_de_mensagens = Listbox(frame, height=25, width=70, yscrollcommand=scrollbar.set)   #Cria uma listbox onde ficarão todas as mensagens
lista_de_mensagens.pack(side=LEFT, fill=BOTH)    #Adiciona a listbox na tela, do lado esquerdo
lista_de_mensagens.pack()

frame.pack()  #Adiciona o frame na tela

entrada = Entry(tk, textvariable=mensagem)   #Cria o local para recebe entrada do usuário
entrada.bind("<Return>", enviar_msg)    #Aceita o Enter como entrada para chamar a função enviar_msg
entrada.pack(side=LEFT, expand=True)   #Adiciona o local

botao_mensagem = Button(tk, text="Enviar", command=enviar_msg)  #Funciona do mesmo jeito que apertar Enter para receber a string escrita
botao_mensagem.pack(side=LEFT)     #Cria o botão na tela do lado esquerdo

botao_pesquisa = Button(tk, text="Pesquisar", command=func_pesquisa)   #Botão para realizar pesquisa
botao_pesquisa.pack(side=LEFT)    

botao_chamada = Button(tk, text="Ligar", command=liga)  #Botão para ligar
botao_chamada.pack(side=LEFT)

botao_chamada = Button(tk, text="Sair", command=sair)   #Botão para sair
botao_chamada.pack(side=LEFT)


tk.protocol("WM_DELETE_WINDOW", fecha_tela)   #Para fechar a tela

TAM_BUFFER = 1024   #Variáveis para socket
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000   #Porta para conexão entre sockets TCP
PORT_AUDIO = 6000   #Porta para conexão entre sockets UDP
ADDR = (HOST, PORT)

socket_audio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Cria o socket com o protocolo UDP


socket_do_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Cria o socket com o protocolo TCP por meio do socket.SOCK_STREAM


socket_do_cliente.connect(ADDR)    #Conecta o socket do usuário na porta 5000
recebe_thread = Thread(target=recebe) 
recebe_thread.start()
mainloop()
