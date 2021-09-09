
from tkinter import *
from threading import *
from functools import partial
import socket
import tkinter
import pyaudio


count = 0

def audio():

    audio_format = pyaudio.paInt16
    channels = 1
    rate = 20000
    
    # SERVER_BIND = (HOST, PORT_AUDIO)

    
    # socket.connect((HOST, PORT_AUDIO))
    # socket_audio.bind((HOST, PORT_AUDIO))

    print(socket_audio)
    AUDIO = pyaudio.PyAudio()
    recebe_stream = AUDIO.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=TAM_BUFFER)
    envia_stream = AUDIO.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=TAM_BUFFER)
    
    recebe_thread = Thread(target=recebe_voz, args=(recebe_stream, socket_audio,))
    transmite_thread = Thread(target=envia_voz, args=(socket_audio, envia_stream,))

    recebe_thread.start()
    transmite_thread.start()


def recebe_voz(recebe_dado, socket):
   
    while True:
        try:
            
            data, servidor = socket.recvfrom(TAM_BUFFER * 4)
            print(data)
            recebe_dado.write(data)
        except:
            pass

def envia_voz(socket, manda_dado):
    while True:
        try:
            
            data = manda_dado.read(TAM_BUFFER)
            #print(data)
            socket.send(data)

        except:
            pass

def aceitar_chamada(janela):
    socket_audio.connect((HOST, PORT_AUDIO))
    janela.destroy()
    audio()



# def recusar_chamada():


def controle_chamada():
    janela_aceita = tkinter.Toplevel()
    janela_aceita.wm_title("Recebendo chamada")
    botao_aceitar = Button(janela_aceita, text="Aceitar", command=lambda: aceitar_chamada(janela_aceita))
    botao_aceitar.pack()

    botao_recursar = Button(janela_aceita, text="Recusar", command= lambda: recusar_chamada(janela_aceita))
    botao_recursar.pack()

def fecha_tela(event=None):  #Fecha a tela pelo X, fazendo o mesmo processo de quando se escreve {sair}
    
    mensagem.set("{sair}")
    enviar_msg()

def recebe():    #Recebe a mensagem do server já tratada
    while True:
        try:
            msg = socket_do_cliente.recv(TAM_BUFFER).decode("utf8")
            if(msg == "recebe_ligacao"):
                resposta = controle_chamada()
            else:
                lista_de_mensagens.insert(END, msg)
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

def enviar_nome(janela):
    msg = "Pesquisa " + mensagem2.get()
    mensagem2.set("")
    janela.destroy()
    socket_do_cliente.send(bytes(msg, "utf8"))


def envia_string(janela):
    msg = "!@#$%" + mensagem2.get()
    mensagem2.set("")
    # janela.destroy()
    socket_do_cliente.send(bytes(msg, "utf8"))
    

def func_pesquisa():
    janela_pesquisa = tkinter.Toplevel()
    janela_pesquisa.wm_title("Pesquisa") 
    entrada_nome = Entry(janela_pesquisa, textvariable=mensagem2)

    entrada_nome.bind("<Return>", enviar_nome)    
    entrada_nome.pack()
    botao_nome = Button(janela_pesquisa, text="Pesquisar", command=lambda:enviar_nome(janela_pesquisa))
    botao_nome.pack()

def sair():
    socket_do_cliente.send(bytes("{sair}", "utf8"))
    socket_do_cliente.close()
    tk.quit()

def conectar_remetente():
    print('conectei')
    audio()

def liga(event=None):
    if(count == 0):
        janela_ligacao = tkinter.Toplevel()
        janela_ligacao.wm_title("Ligar")

        nomePesquisa = Entry(janela_ligacao, textvariable=mensagem2) 
        nomePesquisa.bind("<Return>", envia_string) 
        nomePesquisa.pack(side=LEFT, expand=True)
        
        
        botao_nome = Button(janela_ligacao, text="Ligar", command=lambda:envia_string(janela_ligacao))
        botao_nome.pack()
        socket_audio.bind(('', PORT_AUDIO))
        Thread(target=conectar_remetente).start()
        
        

    else:
        janela_no_name = tkinter.Toplevel()
        janela_no_name.geometry("200x20")
        janela_no_name.wm_title()
        text = Label(janela_no_name, text='Você não digitou seu nome ainda!!!')
        text.pack()
        # mensagem_no_name = 'Você não digitou seu nome ainda!!!'

    # socket_do_cliente.send(bytes('!@#$%'))

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

botao_pesquisa = Button(tk, text="Pesquisar", command=func_pesquisa)
botao_pesquisa.pack(side=LEFT)    

botao_chamada = Button(tk, text="Ligar", command=liga)
botao_chamada.pack(side=LEFT)

botao_chamada = Button(tk, text="Sair", command=sair)
botao_chamada.pack(side=LEFT)


tk.protocol("WM_DELETE_WINDOW", fecha_tela)   #Para fechar a tela

TAM_BUFFER = 1024   #Variáveis para socket
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000 
PORT_AUDIO = 6000   
ADDR = (HOST, PORT)

socket_audio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


socket_do_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Cria o socket com o protocolo TCP por meio do socket.SOCK_STREAM


socket_do_cliente.connect(ADDR)    #Conecta o socket do usuário na porta 5000
print(socket_do_cliente)
recebe_thread = Thread(target=recebe) 
recebe_thread.start()
mainloop()
