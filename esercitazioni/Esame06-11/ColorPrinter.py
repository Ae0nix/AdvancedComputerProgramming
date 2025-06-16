import sys
import stomp
import time

class MyListener(stomp.ConnectionListener):

    def __init__(self, tipo):
        self.tipo = tipo

    def on_message(self, frame):
        message = frame.body

        if tipo in message:
            with open(f"color.txt", "w") as f:
                print(f"[COLOR PRINTER] Received message: {message}")
                f.write(message)



if __name__ == "__main__":
    try:
        tipo = sys.argv[1]
        if (tipo != "doc" and tipo != "txt"):
            sys.exit(-1)
    except IndexError as e:
        print("[BW PRINTER] Usage BwPrinter [bw/gs]")
        sys.exit(-1)

    conn = stomp.Connection([("127.0.0.1", 61613)])
    conn.connect(wait=True)

    conn.set_listener('', MyListener(tipo))
    conn.subscribe(destination="/queue/color", id=1, ack='auto')
    

    while True:
        time.sleep(60)