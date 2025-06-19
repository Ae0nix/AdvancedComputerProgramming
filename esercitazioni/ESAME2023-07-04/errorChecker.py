import time
import sys

import stomp

class MyListener(stomp.ConnectionListener):

    def __init__(self, messaggioLog):
        self.messaggioLog = messaggioLog

    def on_message(self, frame):
        if messaggioLog in frame.body:
            with open("error.txt", "a") as f:
                f.write(frame.body+"\n")
                print(f"[ERROR CHECKER] Ho ricevuto il seguente messaggio {frame.body}")

if __name__ == "__main__":

    try:
        messaggioLog = sys.argv[1]
    except IndexError as e:
        print("Usage error")
        sys.exit(-1)

    conn = stomp.Connection([("localhost", 61613)])
    conn.set_listener('', MyListener(messaggioLog))
    conn.connect(wait=True)

    conn.subscribe(destination='/queue/error', id=1, ack='auto')

    while True:
        time.sleep(60)

    conn.disconnect()