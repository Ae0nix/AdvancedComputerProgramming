from multiprocessing import Lock, Condition

from concurrent import futures
import grpc
import Servizio_pb2 as s_pb2
import Servizio_pb2_grpc as s_pb2_grpc


class Servizio(s_pb2_grpc.ServizioServicer):
    def __init__(self):
        self.queue = []
        self.queue_size = 5

        queue_lock = Lock()
        self.consumer_cv = Condition(lock=queue_lock)
        self.producer_cv = Condition(lock=queue_lock)

    def deposita(self, request, context):
        with self.producer_cv:
            self.producer_cv.wait_for(lambda: self.theres_a_space(self.queue))

            message = str(request.id) + "-" + request.product
            self.queue.append(message)
            print(f"[IMPL] Appended {request.product}: {str(request.id)}")

            self.consumer_cv.notify()
        
        return s_pb2.StringMessage("Deposited")

    def preleva(self, request, context):
        with self.consumer_cv:
            self.consumer_cv.wait_for(lambda: self.theres_an_item(self.queue))

            popped_item = self.queue.pop()

            id = int(popped_item.split("-")[0])
            product = popped_item.split("-")[1]

            self.producer_cv.notify()
        
        return s_pb2.Articolo(id, product)
    

    def svuota(self, request, context):
        with self.consumer_cv:
            self.consumer_cv.wait_for(lambda: self.theres_an_item(self.queue))

            while self.queue:
                popped_item = self.queue.pop()

                id = int(popped_item.split("-")[0])
                product = popped_item.split("-")[1]
                print(f"[IMPL] Svuotato: {id}, {product}")

                yield s_pb2.Articolo(id=id, product=product)

            self.consumer_cv.notify()

        


    def theres_a_space(self, queue):
        return len(queue) != self.queue_size
    
    def theres_an_item(self, queue):
        return len(queue) > 0
    

if __name__ == "__main__":

    server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10), 
            options=(('grpc.so_reuseport', 0),)
        )
    s_pb2_grpc.add_ServizioServicer_to_server(Servizio(), server)

    port = server.add_insecure_port("[::]:50051")
    print('Starting server. Listening on port ' + str(port))

    server.start()

    print("Server running ... ")

    server.wait_for_termination()
