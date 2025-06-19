import socket
import random
import sys

from clientThread import ClientThread
import threading as mt


if __name__ == "__main__":

    try:
        client_type = sys.argv[1]
        port = sys.argv[2]

    except IndexError as e:
        print("Error usage")
        sys.exit(-1)


    threads = []
    for i in range(5):
        print(f"[CLIENT]✅ Starting thread {i}")
        th = ClientThread(client_type, port)
        threads.append(th)
        th.start()

    for thread in threads:
        thread.join()