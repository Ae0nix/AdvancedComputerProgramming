from client.MagazzinoProxy import MagazzinoProxy
import socket
import threading as mt
import random
import sys
import time

NUM_THREAD = 5
NUM_REQUEST = 3
PRODUCT_TYPE = ["laptop", "smartphone"]

def main():

    try:
        host= sys.args[1]
        port = sys.args[2]
        request_type = sys.ars[3]
    except IndexError:
        print("[CLIENT] Missing server port number and host")
        print("[CLIENT] Usage client [host] [port] [A/B]")
        sys.exit(-1)

    threads = []

    for i in range(NUM_THREAD):
        th = mt.Thread(target=thread_func, args = (host, port, request_type))
        threads.append(th)
        th.start()
    
    for t in threads:
        t.join()




def thread_func(host, port, request_type):

    proxy = MagazzinoProxy(host, port)

    for i in range(NUM_REQUEST):
        time.sleep(random.randint(2,4))

        if request_type == "A":
            ### scegliamo un articolo a caso con id a caso
            articolo = PRODUCT_TYPE[random.randint(0,1)]
            id = random.randint(1,100)
            ### chiamiamo la funzione deposita del proxy, devo inizializzare un proxy al quale passare i dettagli della connessione
            response = proxy.deposita(articolo, id)
            ### si potrebbe implementare un meccanismo che controlli la risposta per vedere se è andato tutto a buon fine
            
        elif request_type == "B":
            ### scelgo a caso un articolo
            articolo = PRODUCT_TYPE[random.randint(0,1)]
            ### chiamo la funzione preleva del proxy
            response = proxy.preleva(articolo)

        else:
            print("[CLIENT] An unsopported type of client has been used")
            sys.exit(-1)
    


if __name__ == "__main__":
    main()