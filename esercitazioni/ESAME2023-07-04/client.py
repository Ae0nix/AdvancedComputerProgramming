from clientProxy import ClientProxy
import random
import time
import sys

FIRST_CHOICE = ["success", "checking"]
SECOND_CHOICE = ["fatal", "exception"]

if __name__ == "__main__":

    try:
        host = "localhost"
        port = int(sys.argv[1])
    except IndexError as e:
        print("Usage error")
        sys.exit(-1)

    p = ClientProxy(host, port)

    for i in range(10):
        tipo = random.randint(0,2)

        match tipo:
            case 0 | 1:
                messaggioLog = FIRST_CHOICE[random.randint(0,1)]
            case 2:
                messaggioLog = SECOND_CHOICE[random.randint(0,1)]
        
        p.log(messaggioLog, tipo)
        time.sleep(1)



