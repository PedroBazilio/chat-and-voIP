from tkinter import *
from threading import *
import socket

def fecha_tela(event=None):
    
    mensagem.set("{sair}")
    enviar_msg()

def recebe():
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
frame = Frame()
scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)
mensagem = StringVar()
mensagem.set("")
lista_de_mensagens = Listbox(frame, height=25, width=70, yscrollcommand=scrollbar.set)
lista_de_mensagens.pack(side=LEFT, fill=BOTH)
lista_de_mensagens.pack()
frame.pack()
entrada = Entry(tk, textvariable=mensagem)
entrada.bind("<Return>", enviar_msg)
entrada.pack(side=LEFT, expand=True)
botao_mensagem = Button(tk, text="Enviar", command=enviar_msg)
botao_mensagem.pack(side=LEFT)
tk.protocol("WM_DELETE_WINDOW", fecha_tela)
TAM_BUFFER = 1024
HOST = input("Host: ")
PORT = 5000
ADDR = (HOST, PORT)
socket_do_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_do_cliente.connect(ADDR)
recebe_thread = Thread(target=recebe)
recebe_thread.start()
mainloop()
