from threading import Thread
from Proxy import Proxy
import random
import time

ARTICOLI = ["LAPTOP", "SMARTPHONE"]

class ClientThread(Thread):

    def __init__(self,client_type, port):
        super().__init__()
        self.proxy : Proxy = Proxy(port)
        self.client_type = client_type

    def run(self):

        for i in range(3):

            time_to_wait = random.randint(2,4)
            articolo = ARTICOLI[random.randint(0,1)]

            match self.client_type:
                case "A":
                    time.sleep(time_to_wait)
                    id = random.randint(1,100)
                    
                    print(f"[CLIENT THREAD] Generata una richietsa di deposita con {articolo} e {id}")
                    self.proxy.deposita(articolo, id)
                case "B":
                    print(f"[CLIENT THREAD] Generata una richietsa di preleva con {articolo}")
                    response = self.proxy.preleva(articolo)
                    print(f"[CLIENT THREAD] L'articolo che è stato prelevato ha id: {response.decode("utf-8")}")
