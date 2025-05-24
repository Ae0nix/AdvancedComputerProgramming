import uuid
import logging
from concurrent import futures 

import grpc
import proto.OrderManagment_pb2 as om_pb2
import proto.OrderManagment_pb2_grpc as om_pb2_grpc


# 🔧 Configurazione logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(message)s'
)


#commento per vedere il colore
class OrderManagmentSercice(om_pb2_grpc.OrderManagmentServicer):

    def __init__(self):
        self.orderDict = {}

    def addOrder(self, request, context):
        id = uuid.uuid1() #genero un id basandomi su mac address
        request.id = str(id)
        self.orderDict[request.id] = request
        logging.debug("[server] added order with id: " + request.id)
        return om_pb2.StringMessage(value=request.id)
    
    def getOrder(self, request, context):
        if request.value == None:
            raise ValueError("Richiesta contentente ID mancante o non valido")
        list_of_ids = self.orderDict.keys()
        if request.value in list_of_ids:
            return self.orderDict[request.value]
        else:
            return om_pb2.Order() #questo restituisce un ordine vuoto

    def searchOrders(self, request, context):
        itemFound = 0
        for order in self.orderDict.values():
            if request.value in order.itemList:
                itemFound += 1
                logging.debug("[server] Item " + request.value + " trovato nell'ordine con ID: " + order.id)
                yield order

    
    def processOrders(self, request_iterator, context):
        listOfLocation = set()
        incomingOrders = list()       
        for order in request_iterator:
            listOfLocation.add(order.destination)
            incomingOrders.append(order)

        for destination in listOfLocation:
            ordersDividedByLocation = list()
            for order in incomingOrders:
                if order.destination == destination:
                    ordersDividedByLocation.append(order)
            shipment = om_pb2.Shipment(id=str(uuid.uuid1()), state="PROCESSED", orderList=ordersDividedByLocation)
            yield shipment

def serve():
    """
    Riassunto delle funzionalità di questa funzione
    1. Creo un server gRPC
    2. Registra il gestore del servizio
    3. Faccio scegliere una porta liberamente al sistema
    4. Avvio il server e aspetto la terminazione
    """


    #creo un server grpc
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), #gli diciamo che stiamo usando un threadpool di 10 thread per gestire le richiesete
        options=(('grpc.so_reuseport', 0),) #disabilito l'uso delle porte condivise non permettendo a più processi di ascoltare su stessa porta
        )  
    
    #registriamo un'implementazione concreta del servizio gRPC OrderManagment all'interno del server
    om_pb2_grpc.add_OrderManagmentServicer_to_server(OrderManagmentSercice(), server)

    port = 0
    port = server.add_insecure_port("[::]:" + str(port)) #in questo modo vado a scegliere una porta da dare al server che sarà in ascolto su tutte le interfacce di rete

    logging.info("[server] Server started, listening on port: " + str(port))

    server.start()
    server.wait_for_termination()



if __name__ == "__main__":
    serve()
