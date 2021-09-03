from tkinter import *
from threading import *
import socket
import tkinter
import pyaudio


count = 0

def audio(socket):

    audio_format = pyaudio.paInt16
    channels = 1
    rate = 20000
    
    
    nome = mensagem.get()
    mensagem.set("")
    socket.send(bytes(nome, "utf8"))

    socket_audio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    py_audio = pyaudio.PyAudio()
    playing_stream = pyaudio.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
    recording_stream = pyaudio.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)

    receive_thread = Thread(target=receive_server_data, args=(socket_audio, playing_stream)).start()
    send_data_to_server(socket_audio, recording_stream)




def receive_server_data(socket, play_stream):
    while True:
        try:
            data = socket.recv(1024)
            play_stream.write(data)
        except:
            pass

def send_data_to_server(socket, record_stream):
    while True:
        try:
            data = record_stream.read(1024)
            socket.sendall(data)
        except:
            pass




def fecha_tela(event=None):  #Fecha a tela pelo X, fazendo o mesmo processo de quando se escreve {sair}
    
    mensagem.set("{sair}")
    enviar_msg()

def recebe():    #Recebe a mensagem do server já tratada
    while True:
        try:
            msg = socket_do_cliente.recv(TAM_BUFFER).decode("utf8")
            lista_de_mensagens.insert(END, msg)
            if(msg.startswith('NOME')):
                nome_principal = 
        except OSError:
            break


def enviar_msg(event=None):  #Enviar a mensagem para o server para ser tratada
    count = 1
    print(count)
    msg = mensagem.get()
    mensagem.set("")
    socket_do_cliente.send(bytes(msg, "utf8"))
    if msg == "{sair}":     #Caso a mensagem escrita, pelo cliente e já tratada pelo servidor, seja {sair} o tkinter é fechado 
        socket_do_cliente.close()
        tk.quit()

def liga(event=None):
    print(count)
    if(count == 1):
        janela_ligacao = tkinter.Toplevel()
        janela_ligacao.wm_title()
        nome = StringVar()
        nomePesquisa = Entry(janela_ligacao, textvariable=nome) 
        nomePesquisa.bind("<Return>", enviar_msg) 
        nomePesquisa.pack(side=LEFT, expand=True)
        botao_nome = Button(janela_ligacao, text="Ligar")
        botao_nome.pack()

        #vai receber socket com a mensagen de controle podendo ser:
        #1 - usuario não existe
        #2 - usuario ocupado
        #3 - usuario negou a chamada
        #4 - usuario aceitou a chamada
        #a partir de 4, temos:
        #recebimento de socket tcp com nome e porta do cliente a ser feita a ligação
        # usamos o socket udp com a porta desejada para começar a mandar audio  
        

    else:
        janela_no_name = tkinter.Toplevel()
        janela_no_name.geometry("200x20")
        janela_no_name.wm_title()
        text = Label(janela_no_name, text='Você não digitou seu nome ainda!!!')
        text.pack()
        # mensagem_no_name = 'Você não digitou seu nome ainda!!!'

    # socket_do_cliente.send(bytes('!@#$%'))

nome_principal = ''
tk = Tk()
tk.title("Chat")
frame = Frame()  #Cria um frame

scrollbar = Scrollbar(frame)   #Cria uma scrollbar 
scrollbar.pack(side=RIGHT, fill=Y)   #aAdiciona ela na tela do lado direito preenchendo todo o eixo Y

mensagem = StringVar()    #Variável para receber o valor escrito pelo usuário
mensagem.set("")

lista_de_mensagens = Listbox(frame, height=25, width=70, yscrollcommand=scrollbar.set)   #Cria uma listbox onde ficarão todas as mensagens
lista_de_mensagens.pack(side=LEFT, fill=BOTH)    #Adiciona a listbox na tela, do lado esquerdo
lista_de_mensagens.pack()

frame.pack()  #Adiciona o frame na tela

entrada = Entry(tk, textvariable=mensagem)   #Cria o local para recebe entrada do usuário
entrada.bind("<Return>", enviar_msg)    #Aceita o Enter como entrada para chamar a função enviar_msg
entrada.pack(side=LEFT, expand=True)   #Adiciona o local

botao_mensagem = Button(tk, text="Enviar", command=enviar_msg)  #Funciona do mesmo jeito que apertar Enter para receber a string escrita
botao_mensagem.pack(side=LEFT)     #Cria o botão na tela do lado esquerdo

botao_pesquisa = Button(tk, text="Pesquisar")
botao_pesquisa.pack(side=LEFT)    

botao_chamada = Button(tk, text="Ligar", command=liga)
botao_chamada.pack(side=LEFT)


tk.protocol("WM_DELETE_WINDOW", fecha_tela)   #Para fechar a tela

TAM_BUFFER = 1024   #Variáveis para socket
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000    
ADDR = (HOST, PORT)

socket_do_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Cria o socket com o protocolo TCP por meio do socket.SOCK_STREAM
socket_do_cliente.connect(ADDR)    #Conecta o socket do usuário na porta 5000
recebe_thread = Thread(target=recebe) 
recebe_thread.start()
mainloop()
