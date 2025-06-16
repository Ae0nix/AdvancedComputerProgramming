from clientProxy import ClientProxy
import sys
import time
import random

TIPO = ["gs", "color", "bw"]
ESTENSIONI = ["doc", "txt"]

if __name__ == "__main__":

    try:
        host = "localhost"
        port = int(sys.argv[1])
    except IndexError as e:
        print("[CLIENT] Usage client.py [PORT]")
        sys.exit(-1)

    p = ClientProxy(host, port)

    for i in range(10):
        tipo = TIPO[random.randint(0,2)]
        pathFile = f"/user/file_{random.randint(0,100)}.{ESTENSIONI[random.randint(0,1)]}"

        p.print(pathFile, tipo)
        
        time.sleep(1)