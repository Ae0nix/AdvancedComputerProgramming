import random
import time
import stomp

class MyListener()
    def on_message(self, frame):
        print("frame: ", frame)
        print(f"[CLIENT] ricevuta risposta {frame.body}")



def main():
    pass
    ## comunicazione stomp, devo inviare
    ## si crei i client che genera 10 richieste di tipo deposita, 5 di tipo preleva ed 1 di tipo svuota,
    ## tipo di richiesta, id_articolo e prodotto siano generati in maniera casuale

    #gli oggetti administred objects devono essere istanziati prima di fare la comunicazione


    conn = stomp.Connection([('localhost', 6163)])

    conn.set_listener('', MyListener())

    conn.connect(wait=True)

    conn.subscribe(destination='/queue/response', id=1, ack='auto')

    products = ['smartphone', 'laptop']

    for i in range(15):
        if i< 10:
            request = "deposita"
            id = random.randint(1, 200)
            product = products[(i%2)]
            
            MSG = request + "-" + str(id) + "-" + product
        else:
            MSG = "preleva"
        
        conn.send("/queue/request", MSG)
        print("[CLIENT] request", MSG)

        time.sleep(120)

if __name__ == "__main__":
    main()