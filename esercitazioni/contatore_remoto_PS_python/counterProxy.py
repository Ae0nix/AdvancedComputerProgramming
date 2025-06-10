from ICounter import ICounter
import socket

class CounterProxy(ICounter):
    
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def setCount(self, id, initial_value):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            messageToSend = f"setCount-{id}-{initial_value}"
            s.send(messageToSend.encode("utf-8"))
            print(f"[DEBUG] MESSAGGIO INVIATO: {messageToSend}")

            result = s.recv(1024).decode("utf-8")
            return result
        
    def increment(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            messageToSend = f"increment"
            s.send(messageToSend.encode("utf-8"))
            print(f"[DEBUG] MESSAGGIO INVIATO: {messageToSend}")

            result = s.recv(1024).decode("utf-8")
            return result
    
    def sum(self, increment):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            messageToSend = f"sum-{increment}"
            s.send(messageToSend.encode("utf-8"))
            print(f"[DEBUG] MESSAGGIO INVIATO: {messageToSend}")

            result = s.recv(1024).decode("utf-8")
            return result