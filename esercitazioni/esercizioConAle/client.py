import sys
import random
import threading
from dispatcher_proxy import DispatcherProxy

N_CLIENT = 5
N_REQUEST_FOR_THREAD = 3

def targetFunc(host, port):

    for i in range(N_REQUEST_FOR_THREAD):
        valueToSend = random.randint(0,3)

        proxy = DispatcherProxy(host, port)
        proxy.sendCmd(valueToSend)


def main():
    try:
        HOST = sys.argv[1]
        PORT = sys.argv[2]
    except IndexError:
        print("Provide an Host and a port number")
        sys.exit(-1)
    
    clients = []
    for _ in range(N_CLIENT):

        client = threading.Thread(target=targetFunc, args=(HOST, int(PORT)))
        client.start()

        clients.append(client)


if __name__ == "__main__":
    main()
