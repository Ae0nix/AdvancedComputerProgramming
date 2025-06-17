import ProductManager_pb2 as pm_pb2
import ProductManager_pb2_grpc as pm_pb2_grpc
import grpc
import random
import sys

import threading as mt

def thread_func(i, port):

    host = "localhost"
    channel = grpc.insecure_channel(host + ':' + port)
    stub = pm_pb2_grpc.ProductManagerStub(channel)
    
    if i%2 == 0:
        #sell
        random_id = random.randint(1,100)
        print(f"[USER] Sending sell request with {random_id}")
        result = stub.sell(pm_pb2.SellingRequest(serial_number=random_id))
        if result.value:
            print("[USER] ACK received")
        else:
            print("[USER] Something went wrong")
        
    else:
        #buy
        print(f"[USER] Sending buy request")
        result = stub.buy(pm_pb2.Empy())
        print(f"[USER] Extracted ID: {str(result.serial_number)}")


if __name__ == "__main__":

    try:
        port = sys.argv[1]
    except IndexError as e:
        print("[CLIENT] Usage User.py [PORT]")
        sys.exit(-1)
    threads = []
    for i in range(10):
        th = mt.Thread(target=thread_func, args=(i, port))
        threads.append(th)
        th.start()


    for thread in threads:
        thread.join()