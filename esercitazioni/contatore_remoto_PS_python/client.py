from counterProxy import CounterProxy
import sys
import random

import threading as mt

POSSIBLE_METHOD=["setCount", "sum", "increment"]
NUM_REQ = 4
NUM_THREAD = 3

def runFunction(id, host, port):
    proxy = CounterProxy(host, port)

    for _ in range(NUM_REQ):
        random_function = random.randint(0,2)

        match random_function:
            case 0:
                valueToSet = 0
                print(f"[CLIENT] Send setCount() message from client with id: {id} set value: {valueToSet}")
                counterValue = proxy.setCount(id, valueToSet)
                print(f"\t Value of counter: {counterValue}")

            case 1:
                valueToBeSummed = random.randint(1,5)
                print(f"[CLIENT] Send sum() message from client with id: {id} set value to be summed: {valueToBeSummed}")
                counterValue = proxy.sum(valueToBeSummed)
                print(f"\t Value of counter: {counterValue}")

            case 2:
                print(f"[CLIENT] Send increment() message from client with id: {id}")
                counterValue = proxy.increment()
                print(f"\t Value of counter: {counterValue}")



def main():

    # try:
    #     host = "localhost"
    #     port = int(sys.argv[1])
    # except IndexError:
    #     print("Usage: client.py [PORT_NUMBER]")
    port = 55348
    host = "localhost"


    threads = []
    for i in range(NUM_THREAD):
        th = mt.Thread(target=runFunction, args=(i, host, port))
        th.start()
        

    # for thread in threads:
    #     thread.join()




if __name__ == "__main__":
    main()