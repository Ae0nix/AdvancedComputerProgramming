from dispatcher_service import DispatcherService
import socket
import sys
import logging 

import multiprocessing as mp 

def processFunc(conn, skeleton):
    message = conn.recv(1024)
    logging.debug("[DISPATCHER] Message received: " + message.decode("utf-8"))

    request = (message.decode('utf-8')).split('-')[0]
    logging.debug("[DispatcherSkeleton run_function] request received: ", request)

    if request == "sendCmd":
        value_to_send = (message.decode("utf-8")).split()[1]
        logging.debug("[DispatcherSkeleton run_function] request is sendCmd, value is: ", value_to_send)
        skeleton.sendCmd(value_to_send)
        result = "ACK"
    else:
        logging.debug("[DispatcherSkeleton run_function] request is getCmd...wait for result")
        result = skeleton.getCmd()
    
    logging.debug("[DispatcherSkeleton run_function] result to send back: ", result)
    conn.send(result.encode("utf-8"))

    conn.close()

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
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            logging.info("[SERVER] Server started on port: " + str(s.getsockname()[1]))
            s.listen(5)

            logging.debug("[SERVER] server is listening")
            while True:
                conn, addr = s.connect()
                logging.debug('Connected to :', addr[0], ':', addr[1])

                p = mp.Process(target=processFunc, arg=(conn, self))
                p.start()
