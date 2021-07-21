from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter.constants import Y

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)#forma do tkinter mostrar mensagens antigas
        except OSError:
            break


def send(event = None):
    # event é passada por "binders"
    #lida com o envio das mensagens
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        root.quit()


def closing(event = None): #chamada na quanda a janela fecha 
    my_msg.set("{quit}")
    send()


root = tkinter.Tk()
root.title('TheChatter')


messages_frame = tkinter.Frame(root)
my_msg = tkinter.StringVar() # para as mensagens que serão enviadas
my_msg.set("Digite suas mensagens aqui.")
scrollbar = tkinter.Scrollbar(messages_frame) # para navegar entre as mensagens

msg_list = tkinter.Listbox(messages_frame, height=15, width=50,
yscrollcommand=scrollbar.set)

scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages_frame.pack()


#para o envio de mensagens
entry = tkinter.Entry(root, textvariable=my_msg)
entry.bind("<Return>", send)
entry.pack()
send_button = tkinter.Button(root, text="Send", command=send)
send_button.pack()
root.protocol("WM_DELETE_WINDOW", closing)



#Pegamos o endenreço e criamos um socket para conecta-lo
HOST = input("Entre com o host:")
PORT = input("Entre com a porta:")

if not PORT:
    PORT = 33000 #Valor default
else:
    PORT = int (PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

#inicio da thread para recebimento das mensagens
receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()









