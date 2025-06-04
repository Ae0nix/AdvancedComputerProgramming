from threading import Thread
import socket
from sys import exit

class SkeletonThread(Thread):
    
    def __init__(self, conn, ref):
        super().__init__()
        self.conn : socket.socket = conn
        self.ref = ref
        self.buf_size = 1024

    def run(self):
        message = self.conn.recv(self.buf_size)
        split_message = message.split(",")

        article = split_message[1]

        if split_message[0] == "preleva":
            ### chiama la funzione preleva del server
            result = self.ref.preleva(article)
        elif split_message[0] == "deposita":
            ### chiama la funzione deposita del server
            id = split_message[2]
            result = self.ref.deposita(article, id)
        else:
            print("[SKELETON THREAD] Error operation not recognized")
            exit(-1)

        self.conn.sendall(result.encode()) #non c'è bisogno di fare sendto perché essendo TCP ho stabilito una connessione
        print("[SKELETON THREAD] Result sent")
