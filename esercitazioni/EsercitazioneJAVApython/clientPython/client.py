import sys
import time
import stomp
import random

RICHIESTE = ["DEPOSITA", "PRELEVA"]


class MyListener(stomp.ConnectionListener):
    def on_message(self, frame):
        print('received a message "%s"' % frame.body)


if __name__ == "__main__":
    conn = stomp.Connection([("localhost", 61613)])
    conn.set_listener('', MyListener())
    conn.connect(wait=True)

    conn.subscribe(destination='/queue/response', id=1, ack='auto')
    
    for i in range(10):
        request = RICHIESTE[random.randint(0,1)]

        if request == "DEPOSITA":
            id = random.randint(1,50)
            message_to_send = f"{request}-{id}"
        elif request == "PRELEVA":
                message_to_send = f"{request}"

        conn.send(body=message_to_send, destination='/queue/request', headers={"reply-to":"/queue/response"})
        print(f"[CLIENT] Ho inviato una richiesta al dispatcher: {message_to_send}")

    """
    il messaggio di risposta contiene "deposited" nel caso di richieste DEPOSITA
    oppure il valore prelevato nel caso di richieste PRELEVA
    """
    
    time.sleep(60)
    
    
    conn.disconnect()