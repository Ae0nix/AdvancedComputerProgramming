import time

import multiprocessing as mp
import stomp
import sys
import grpc
import Servizio_pb2 as s_pb2
import Servizio_pb2_grpc as s_pb2_grpc

def process_function(body, host, port):
    channel = grpc.insecure_channel(f"{host}:{port}")
    stub = s_pb2_grpc.ServizioStub(channel)


    conn = stomp.Connection([('127.0.0.1', 61613)])
    conn.set_listener('', MyListener())
    conn.start()

    conn.connect('admin', 'password', wait=True)


    message = body.split("-")
    listOfProduct = list()

    match message[0]:
        case "deposita":
            id = int(message[1])
            product = message[2]
            result = stub.deposita(s_pb2.Articolo(id, product))
            conn.send(destination="/queue/response", body=result.value)
        case "preleva":
            result = stub.preleva()
            message = str(result.id) + "-" + result.product
            conn.send(destination="/queue/response", body=message)
        
        case "svuota":
            
            for result in stub.svuota():
                product = str(result.id) + "-" + result.product
                listOfProduct.append(product)

            for item in listOfProduct:
                conn.send(destination="/queue/response", body=item)

    channel.close()


class MyListener(stomp.ConnectionListener):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def on_message(self, frame):
        proc = mp.Process(target=process_function, args=(frame.body, self.host, self.port))
        proc.start()




if __name__ == "__main__":

    host = "localhost"
    try:
        port = sys.argv[1]
    except IndexError:
        print("[DISPATCHER] Usage dispatcer.py [porta del server]")
        sys.exit(-1)


    conn = stomp.Connection([('127.0.0.1', 61613)])
    conn.set_listener('', MyListener(host, port))


    conn.connect(wait=True)

    conn.subscribe(destination="/queue/richieste", id = 1, ack='auto')




    while True:
        time.spleep(60)


    conn.disconnect()