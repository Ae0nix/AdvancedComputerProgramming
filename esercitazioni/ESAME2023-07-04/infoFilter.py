import time
import sys

import stomp

class MyListener(stomp.ConnectionListener):

    def on_message(self, frame):
        if "1" in frame.body:
            with open("info.txt", "a") as f:
                f.write(frame.body+"\n")
                print(f"[INFO CHECKER] Ho ricevuto il seguente messaggio {frame.body}")

if __name__ == "__main__":


    conn = stomp.Connection([("localhost", 61613)])
    conn.set_listener('', MyListener())
    conn.connect(wait=True)

    conn.subscribe(destination='/queue/info', id=1, ack='auto')

    while True:
        time.sleep(60)

    conn.disconnect()