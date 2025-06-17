import ProductManager_pb2 as pm_pb2
import ProductManager_pb2_grpc as pm_pb2_grpc
import grpc
import requests
from concurrent import futures
from threading import Lock, Condition

PORT = 5001
BASE_URL = "http://localhost:" + str(PORT)



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pm_pb2_grpc.add_ProductManagerServicer_to_server(ProductManagerServicer(), server)
    port = server.add_insecure_port("[::]:0")
    server.start()
    print(f"[PRODUCT MANAGER] Server started on port {str(port)}")
    server.wait_for_termination()
    



class ProductManagerServicer(pm_pb2_grpc.ProductManagerServicer):
    def __init__(self):
        self.queue = []
        self.max_size = 5

        self.lock = Lock()
        self.cv_producer = Condition(self.lock)
        self.cv_consumer = Condition(self.lock)

    def buy(self, request, context):
        with self.cv_consumer:
            self.cv_consumer.wait_for(lambda: self.theres_an_item(self.queue))

            value_to_return = self.queue.pop()

            print(f"[PRODUCT MANAGER] Extracted the following ID from the queue: {value_to_return}")
            
            request_dictionary = {
                "operation": "buy",
                "serial_number": value_to_return
            }

            try:
                response = requests.post(url=BASE_URL + "/update_history", json=request_dictionary)
                response.raise_for_status() #SOLLEVA ECCEZIONE SE HTTP RITORNA ERRORE

            except requests.exceptions.RequestException as e:
                print(f"Error returned from flask server {e}")
            else:
                return pm_pb2.Product(serial_number=value_to_return)
            finally:
                self.cv_producer.notify()



    
    def sell(self, request, context):
        with self.cv_producer:
            self.cv_producer.wait_for(lambda: self.theres_a_space(self.queue))

            serial_number = request.serial_number
            self.queue.append(serial_number)
            print(f"[PRODUCT MANAGER] Put the following id in the queue: {str(serial_number)}")


            request_dictionary = {
                "operation":"sell",
                "serial_number": serial_number
            }

            try:
                response = requests.post(url = BASE_URL + "/update_history", json=request_dictionary)
                response.raise_for_status() #SOLLEVA ECCEZIONE SE IL SERVER RESTITUISCE ERRORE        

                # print(f"Successo! Status: {response.status_code}")
                # print("Risposta dal server:", response.json())
            except requests.exceptions.RequestException as e:
                print(f"Request error {e}")
                return pm_pb2.ACK(value=False)
            else:
                return pm_pb2.ACK(value=True)
            finally:
                self.cv_consumer.notify()
    

    def theres_a_space(self, queue):
        return len(queue) != self.max_size
    
    def theres_an_item(self, queue):
        return len(queue) > 0

if __name__ == "__main__":
    serve()