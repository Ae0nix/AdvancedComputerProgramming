import stomp
import random
import time

NUMBER_OF_MESSAGES = 10

class MyListener(stomp.ConnectionListener):
    def on_error(self, frame):
        print(f"received an error {frame.body}")

    def on_message(self, frame):
        print(f"received a message {frame.body}")




def main():
    conn = stomp.Connection('127.0.0.1', 61613)
    conn.set_listener('', MyListener())
    conn.connect(wait=True)
    conn.subscribe(destination='/queue/response', id = 1, ack='auto')

    for i in range(NUMBER_OF_MESSAGES):
        tipo = random.randint(0,1)
        if tipo == 0:
            tipo_stringa = "deposita"
        elif tipo == 1:
            tipo_stringa = "preleva"

        id_articolo = random.randint(1,100)
        conn.send(body=tipo_stringa + "-" + str(id_articolo), destination='/queue/request')

        time.sleep(60)

    conn.disconnect()

if __name__ == "__main__":
    main()