from ICounter import ICounter
from serverThread import serverThread
import socket

import threading as mt

class CounterSkeleton(ICounter):
    def __init__(self, impl, host="localhost", port=0):
        self.impl : ICounter = impl
        self.host = host
        self.port = port

    def sum(self, increment):
        return self.impl.sum(increment)
    
    def increment(self):
        return self.impl.increment()

    def setCount(self, id, initial_value):
        return self.impl.setCount(id, initial_value)
    
    def run_function(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            print(f"[SKELETON] Server started on port {s.getsockname()[1]}")

            s.listen(10)

            threads = [] #superfluo

            while True:
                conn, addr = s.accept()
                print("[DEBUG] Ricevuta connessione correttamente da parte di un client, la affido ad un thread")
                th = mt.Thread(target=serverThread, args=(self, conn)) 
                th.start()
                threads.append(th)


            for thread in threads:
                thread.join()