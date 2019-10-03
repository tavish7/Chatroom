import socket
from threading import Thread


# Defining Containers Sockets 
clients={}
addresses={}

HOST = "127.0.0.1"
PORT = 1242
buffer= 512

ADDR=(HOST,PORT)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(ADDR)


# ## A Server has three basic jobs--
# #### 1) Accepting New Connections 
# #### 2) Handling CLients
# #### 3) Broadcasting Message



def acc_connections():
    while True:
        client,client_address = s.accept()
        print(f"{client_address} has connected.")
        client.send("Hi".encode('utf-8'))
        client.send("Your Name ".encode('utf-8'))
        addresses[client]= client_address
        Thread(target=handle_client, args=(client, client_address)).start()



def handle_client(conn,addr):         #conn is the client socket
    name=conn.recv(buffer).decode('utf-8')
    welcome = 'Welcome %s! If you ever want to quit, type #quit to exit.' % name
    conn.send(bytes(welcome, "utf-8"))
    msg = "%s from [%s] has joined the chat!" % (name, "{}:{}".format(addr[0], addr[1]))
    broadcast(bytes(msg, "utf8"))                         #sending message to all other clients
    clients[conn] = name
    while True:
        msg = conn.recv(buffer)
        if msg != bytes("#quit", "utf8"):
            broadcast(msg, name + ": ")
        else:
            conn.send(bytes("#quit", "utf8"))
            conn.close()
            del clients[conn]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):                    # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


if __name__ == "__main__":
    s.listen(8)  # Listens for 5 connections at max.
    print("Chat Server has Started !!")
    print("Waiting for connections...")
    ACCEPT_THREAD = Thread(target=acc_connections)
    ACCEPT_THREAD.start()                                             # Starts the infinite loop.
    ACCEPT_THREAD.join()
    s.close()