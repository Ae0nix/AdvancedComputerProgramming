from IMagazzino import IMagazzino
import socket

class Proxy(IMagazzino):

    def __init__(self, port):
        self.port = port


    def deposita(self, articolo, id):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            message_to_send = f"DEPOSITA-{articolo}-{id}"
            s.settimeout(10)

            s.sendto(message_to_send.encode("utf-8"), ("localhost", int(self.port)))
            print("[PROXY]✅ Sent a request to server")

            try:
                msg, addr = s.recvfrom(1024)
            except socket.timeout:
                print("[PROXY]❌ Timeout occurred")
                return
            response = msg.decode("utf-8")
            if response == "ACK":
                print("[PROXY]✅ Andato tutto a buon fine")
            else:
                print("[PROXY]❌ Something went wrong")
                                

    
    def preleva(self, articolo):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            message_to_send = f"PRELEVA-{articolo}"
            s.settimeout(10)


            s.sendto(message_to_send.encode("utf-8"), ("localhost", int(self.port)))
            print("[PROXY]✅ Sent a preleva request to server")

            try:
                msg, addr = s.recvfrom(1024)
            except socket.timeout:
                print("[PROXY]❌ Timeout occurred")
                return None
            response = msg.decode("utf-8")
            return response
    