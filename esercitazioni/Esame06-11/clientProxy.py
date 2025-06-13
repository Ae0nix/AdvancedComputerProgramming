from IPrinter import IPrinter
import socket

class ClientProxy(IPrinter):
    
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def print(self, pathFile, tipo):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            message_to_send = f"{pathFile}#{tipo}"
            s.send(message_to_send.encode("utf-8"))

            print(f"[PROXY] Sent the following request: {pathFile}#{tipo}")

            result = s.recv(1024).decode("utf-8")
            print(f"[PROXY] received from server: {result}")

            return result