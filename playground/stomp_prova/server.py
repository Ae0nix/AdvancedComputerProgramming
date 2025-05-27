import stomp
import time

class MyListener(stomp.ConnectionListener):
    #inizializzare la connessione
    def __init__(self, conn):
        self.conn = conn

    # Metodo che viene invocato alla ricezione di ogni messaggio sulla desination di riferimento
    def on_message(self, frame):
        print(f"Ho ricevuto questo messaggio: {frame.body}")


if __name__ == "__main__":

    conn = stomp.Connection([('127.0.0.1', 61613)])
    
    conn.set_listener('nome', MyListener(conn))

    conn.connect(wait=True) #Attende il completamento della connessione prima di ritornare
    conn.subscribe(destination="/queue/test", id=1, ack='auto')

    time.sleep(10)


    conn.disconnect()