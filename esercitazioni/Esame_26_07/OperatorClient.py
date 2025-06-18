import stomp
import sys
import threading as mt
import time
import random

USERNAME = ["Giggin", "Marotta", "Spiderman", "Iron Man"]


def run_function(i, conn, operator):
    
    #CREATE
    if i < 4:
        client = USERNAME[i]
        hotel = "California"
        nights = random.randint(1,10)
        people = random.randint(1,6)
        cost = random.randint(50, 300)
        request = f"CREATE-{client}-{hotel}-{operator}-{str(nights)}-{str(people)}-{str(cost)}"

        print(f"[OPERATOR] Sent the following CREATE request: {request}")
        conn.send(body=request, destination="/topic/request")
    #UPDATE
    else:
        discount = random.randint(10, 50)
        night = random.randint(1,10)

        request = f"UPDATE-{str(discount)}-{str(operator)}-{str(nights)}"

        print(f"[OPERATOR] Sent the following UPDATE request: {request}")
        conn.send(body=request, destination="/topic/request")


class MyListener(stomp.ConnectionListener):

    def on_message(self, frame):
        print('[OPERATOR] received a message "%s"' % frame.body)



if __name__ == "__main__":

    try:
        operator = sys.argv[1]
    except IndexError as e:
        print("U")


    conn = stomp.Connection([("127.0.0.1", 61613)])
    conn.set_listener('', MyListener())
    conn.connect(wait=True)
    conn.subscribe(destination="/topic/response", id=1, ack='auto')

    
    threads = []
    for i in range(6):
        th = mt.Thread(target=run_function, args=(i, conn, operator))
        th.append()
        th.start()
    

    time.sleep(60)

    for thread in threads:
        thread.join()

    conn.disconnect()
