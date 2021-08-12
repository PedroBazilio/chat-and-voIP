from tkinter import *
from threading import *
import socket

def fecha_tela(event=None):
    
    mensagem.set("{sair}")
    enviar_msg()

def recebe():    #
    while True:
        try:
            msg = socket_do_cliente.recv(TAM_BUFFER).decode("utf8")
            lista_de_mensagens.insert(END, msg)
        except OSError:
            break


def enviar_msg(event=None):
    msg = mensagem.get()
    mensagem.set("")
    socket_do_cliente.send(bytes(msg, "utf8"))
    if msg == "{sair}":
        socket_do_cliente.close()
        tk.quit()


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
tk.protocol("WM_DELETE_WINDOW", fecha_tela)   #Para fechar a tela
TAM_BUFFER = 1024
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5000
ADDR = (HOST, PORT)
socket_do_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Cria o socket com o protocolo TCP por meio do socket.SOCK_STREAM
socket_do_cliente.connect(ADDR)    #Conecta o socket do usuário
recebe_thread = Thread(target=recebe) 
recebe_thread.start()
mainloop()
