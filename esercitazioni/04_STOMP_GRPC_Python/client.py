import time
import random

import stomp

NUMERO_DEPOSITA = 10
NUMERO_PRELEVA = 5
NUMERO_SVUOTA = 1

PORDOTTI = ["laptop", "smartphone"]

class MyListener(stomp.ConnectionListener):
    def on_message(self, frame):
        print(f"received a message {frame.body}")


if __name__ == "__main__":
    conn = stomp.Connection([('127.0.0.1', 61613)])
    conn.set_listener('', MyListener())
    conn.start()

    conn.connect('admin', 'password', wait=True)

    conn.subscribe(destination="/queue/risposta", id = 1, ack='auto')

    for i in range(NUMERO_DEPOSITA):
        random_id = random.randint(1,100)
        message_to_send = "deposita-" + str(random_id) + "-" + PORDOTTI[random.randint(0,1)]
        conn.send(body=message_to_send, destination="/queue/richieste")

    for i in range(NUMERO_PRELEVA):
        random_id = random.randint(1,100)
        message_to_send = "preleva"
        conn.send(body=message_to_send, destination="/queue/richieste")
        

    
    random_id = random.randint(1,100)
    message_to_send = "svuota"
    conn.send(body=message_to_send, destination="/queue/richieste")

    while True:
        time.sleep(60)

    conn.disconnect()