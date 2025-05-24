import grpc
import service_pb2_grpc
import service_pb2

from concurrent import futures

class ServiceImpl(service_pb2_grpc.ServiceServicer()):
    def __init__(self, queue, lock_d, lock_p):
        self.queue = queue 
        self.lock_d = lock_d
        self.lock_p = lock_p
        
    def deposita(self, request, context):
        with self.lock_d:
            ### put.reuqest.id
            self.queue.put([request.id_articolo, request.product])
            print("[SERVER] deposita fatto...")
            return service_pb2.StringMessage(value="depositated")
    
    def preleva(self, request, context):
        with self.lock_p:
            item = self.queue.get()
            return service_pb2.Item(id_articolo=item[0], product=item[1])

    
    def svuota(self, request, context):
       
        self.lock_d.acquire()
        self.lock_p.acquire()

        while not self.queue.empty():
            print("[SERVER] cleaning the queue")
            item = self.queue.get()
            yield service_pb2.Item(id_articolo=item[0], product=item[1])
            
        print("[SERVER] queue is empty")

        self.lock_p.acquire()
        self.lock_d.acquire()


if __name__ ="__main__":
    queue = mp.Queue(5)
    ### creo i lock
    lock_d = mp.Lock()
    lock_d = mp.Lock()

    ### cambia come vado a creare i processi se con spawn, forkserver oppure clone

    ### creo il server grpc che servirà le mie rpc ocn un ThreadPoolExecutor di concurrent
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)
    service_pb2_grpc.add_ServiceServicer_to_server(ServiceImpl(), server)
    port = server.add_insecure_port("[::]:0")

    print("Sever grpc in ascolto su porto: ", port)
    server.start()
    server.wait_for_termination()
