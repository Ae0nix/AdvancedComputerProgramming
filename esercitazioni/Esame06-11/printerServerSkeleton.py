from IPrinter import IPrinter
from abc import ABC, abstractmethod
import socket

import stomp
import multiprocessing as mp 

def process_func(conn, skeleton):
    message = conn.recv(1024).decode("utf-8")

    if message:
        print("[SKELETON] Message received correctly from the client")
        conn.send("ACK".encode("utf-8"))

    path_file = message.split("#")[0]
    tipo = message.split("#")[1]

    skeleton.print(path_file, tipo)


def Consumatore(skeleton):
    conn = stomp.Connection([("127.0.0.1", 61613)])
    conn.connect(wait=True)

    while True:
        
        request = skeleton.consuma()
        
        tipo_richiesta = request.split('-')[1]
        if tipo_richiesta == "color":
            queue_name = "/queue/color"
        else:
            queue_name = "/queue/bw"

        conn.send(body=request, destination=queue_name)




class MyListener():
    def on_message(self, frame):
        print('received a message "%s"' % frame.body)


class printerServerSkeleton(IPrinter, ABC):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    
    @abstractmethod
    def print(self, pathFile, tipo):
        pass

    def run_func(self):
        cons = mp.Process(target=Consumatore, args=(self,))
        cons.start()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))

            print(f"[SKELETON] Server started on port: {s.getsockname()[1]}")

            s.listen(10)

            while True:
                conn, addr = s.accept()

                p = mp.Process(target=process_func, args=(conn, self))
                p.start()

