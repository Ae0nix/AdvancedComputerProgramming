from IPrinter import IPrinter
from abc import ABC, abstractmethod
import socket

import stomp
import multiprocessing as mp 

def process_func(conn, skeleton):
    message = conn.recv(1024)

    path_file = message.split("#")[0]
    tipo = message.split("#")[1]

    skeleton.print(path_file, tipo)



class MyListener():
    def on_message(self, frame):
        print('received a message "%s"' % frame.body)


class printerServerSkeleton(ABC, IPrinter):
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    @abstractmethod
    def print(self, pathFile, tipo):
        pass

    def run_func(self):
        # conn = stomp.Connection()
        # conn.set_listener('', MyListener())
        # conn.connect(wait=True)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))

            print(f"[SKELETON] Server started on port: {s.getsockname()[1]}")

            s.listen(10)

            while True:
                conn, addr = s.accept()

                p = mp.Process(target=process_func, args=(conn, self))
                p.start()

