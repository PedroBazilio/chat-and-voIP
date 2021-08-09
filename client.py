
import socket
from threading import Thread
import tkinter


def receive():
    """Para o recebimento de mensagens."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Perda de conexão com o cliente.
            break


def send(event=None):  # evento é passado por 'binders'.
    """Lida com o envio de mensagens."""
    msg = my_msg.get()
    my_msg.set("")  # Limpa o campo input.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{sair}":
        client_socket.close()
        root.quit()

def close(event=None):
    
    my_msg.set("{sair}")
    send()

root = tkinter.Tk()
#root.geometry('600x1000')
root.title("The Grand Chat")

messages_frame = tkinter.Frame(root)
my_msg = tkinter.StringVar()  # Para as mensagens a serem enviadas.
my_msg.set("Digite suas mensagens aqui.")
scrollbar = tkinter.Scrollbar(messages_frame)  # Para navegar por mensagens antigas.
# Compartimento das mensagens abaixo.
msg_list = tkinter.Listbox(messages_frame, height=25, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(root, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(root, text="Send", command=send)
send_button.pack()

root.protocol("WM_DELETE_WINDOW", close)

#----Parte relacionada aos sockets----
HOST = input("Host: ")
PORT = 5000

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
