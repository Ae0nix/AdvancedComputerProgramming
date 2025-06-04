from IMagazzino import IMagazzino
import socket

class MagazzinoProxy(IMagazzino):
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.buf_size = 1024

    def deposita(self, articolo, id):
        with socket.socket(socket.SOCK_STREAM, socket.AF_INET) as s:
            s.connect(self.host, self.port)

            message_to_send = "deposita," + articolo + "," + id

            s.sendall(message_to_send)

            print(f"[PROXY] Message sent to server: deposita, {articolo}, {id}")

            response = s.recv(self.buf_size).decode()

            return response


    
    def preleva(self, articolo):
        ### Qua essendo per delega mi serve un'istanza dell'implementazione da poter chiamare
        with socket.socket(socket.SOCK_STREAM, socket.AF_INET) as s:
            s.connect(self.host, self.port)

            message_to_send = "preleva," + articolo

            s.sendall(message_to_send)

            print(f"[PROXY] Message sent to server: preleva, {articolo}, {id}")

            response = s.recv(self.buf_size).decode()

            return response