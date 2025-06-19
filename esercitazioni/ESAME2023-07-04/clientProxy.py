from ILogging import ILogging
import random
import socket

class ClientProxy(ILogging):

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def log(self, messaggioLog, tipo):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            messsage_to_send = f"{messaggioLog}-{str(tipo)}"

            s.send(messsage_to_send.encode("utf-8"))
            print(f"[PROXY] Successfully sent message to server: {messsage_to_send}")