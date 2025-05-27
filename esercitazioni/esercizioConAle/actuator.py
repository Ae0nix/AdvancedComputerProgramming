import sys
import threading as mt
from datetime import datetime
from dispatcher_proxy import DispatcherProxy   

def main():
    try:
        HOST = sys.argv[1]
        PORT = sys.argv[2]
    except IndexError:
        print("Please, specify HOST/PORT args...")
        sys.exit(-1)

    
    cmd_dict = {0:"leggi", 1:"scrivi", 2:"configura", 3:"reset"}    
    i = 0

    while True:

        ### l'oggetto proxy potrebbe essere creato una sola volta a meno che non si stabilisce che crei la socket lato client
        proxy = DispatcherProxy(HOST, int(PORT))
        data = proxy.getCmd()
                
        with open("cmdLog.txt", mode="a") as cmdlog_file:
            cmdlog_file.write(f'{datetime.now()} {cmd_dict[int(data)]}\n')
        
        i = i + 1


if __name__ == "__main__":
    main()