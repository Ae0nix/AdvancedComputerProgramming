from dispatcher_service import DispatcherService
import socket
import sys
import logging 

import multiprocessing as mp 

def processFunc(conn, skeleton):
    message = conn.recv(1024)
    logging.debug("[DISPATCHER] Message received: " + message.decode("utf-8"))



    # if data è una send chiama la send
    
    # if data è una get chiama la get

    connection.close()

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


class DispatcherSkeleton(DispatcherService):

    def __init__(self, host, port, dispatcher_service):
        self.host = host
        self.port = port
        self.dispatcher_service = dispatcher_service
    
    def getCmd(self):
        return self.dispatcher_service.getCmd()

    def sendCmd(self, command):
        self.dispatcher_service.sendCmd(command)
    
    def runSkeleton(self):
        with socket.socket(family=AF_INET, socket.SOCK_STREAM):
            s.bind((self.host, self.port))
            logging.info("[SERVER] Server started on port: " + str(s.getsockname()[1]))
            s.listen(5)

            logging.debug("[SERVER] server is listening")
            while True:
                conn, addr = s.connect()
                logging.debug('Connected to :', addr[0], ':', addr[1])

                p = mp.Process(target=processFunc, arg=(conn, self))
                p.start()


        








