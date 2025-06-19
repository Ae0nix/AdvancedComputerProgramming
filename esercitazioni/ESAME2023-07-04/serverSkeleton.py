from ILogging import ILogging
from abc import ABC, abstractmethod
import multiprocessing as mp
import socket
import stomp


def consumatore(skeleton):
    conn = stomp.Connection([("localhost", 61613)])
    conn.connect(wait=True)

    while True:
        message_to_send = skeleton.consuma()
        
        tipo = int(message_to_send.split("-")[1])
        
        if tipo == 2:
            conn.send(body=message_to_send, destination='/queue/error')
        else:
            conn.send(body=message_to_send, destination='/queue/info')
        print("[SKELETON CONSUMATORE] Mandato un messaggio nella coda stomp")



class ServerSkeleton(ILogging, ABC):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @abstractmethod
    def log(self, messaggioLog, tipo):
        pass

    @abstractmethod
    def consuma(self):
        pass

    def run(self):
        ### Lancio il processo consumatore che viene eseguito all'avvio del server
        cons_p = mp.Process(target=consumatore, args=(self,))
        cons_p.start()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))

            print(f"[SKELETON] The server correctly started on port {s.getsockname()[1]}")

            s.listen(10)
            
            while True:
                conn, addr = s.accept()

                message_received = conn.recv(1024).decode("utf-8")
                print(f"[SKELETON] Message correctly received from Proxy: {message_received}")

                messaggio_log = message_received.split("-")[0]
                tipo = message_received.split("-")[1]

                self.log(messaggio_log, tipo)
            


