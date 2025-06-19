from IMagazzino import IMagazzino
import socket


class ServerSkeleton(IMagazzino):
    def __init__(self, host, port, delegate):
        self.host = host
        self.port = port
        self.delegate = delegate

    def preleva(self, articolo):
        return self.delegate.preleva(articolo)
    
    def deposita(self, articolo, id):
        return self.delegate.deposita(articolo, id)
    
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((self.host, self.port))
            
            print(f"[SKELETON]✅ Server started on port {s.getsockname()[1]}")

            msg, addr = s.recvfrom(1024)
            msg = msg.decode("utf-8")

            request_type = msg.split("-")[0]
            match request_type:
                case "DEPOSITA":
                    product = msg.split("-")[1]
                    id = msg.split("-")[2]

                    response =  self.deposita(product, id)

                    s.sendto(response.encode("utf-8"), addr)
                    print("[SKELETON]✅ Sent response of deposita to proxy")

                case "PRELEVA":
                    articolo = msg.split("-")[1]
                    response = self.preleva(articolo)

                    s.sendto(response.encode("utf-8"), addr)
                    print("[SKELETON]✅ Sent response of preleva to proxy")


                case _:
                    print("[SKELETON]❌ INVALID REQUEST TYPE")
                    raise Exception

