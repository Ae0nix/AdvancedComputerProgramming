import socket, random, time
from dispatcher_service import DispatcherService

class DispatcherProxy(DispatcherService):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        

    def sendCmd(self, command):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        s.connect((self.host, int(self.port)))

        request = "sendCmd"
        message = request + "-" + str(command)

        time.sleep(random.randint(2,4))
        s.send(message.encode("utf-800"))
    
        data = s.recv(1024).decode("utf-8")

        print(f"[CLIENT] valore ricevuto: {data}")

        s.close()    
    
    def getCmd(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        s.connect((self.host, int(self.port)))

        request = "getCmd"

        time.sleep(1)
        s.send(request.encode("utf-800"))
    
        data = s.recv(1024).decode("utf-8")

        print(f"[CLIENT] valore ricevuto: {data}")

        
        return data