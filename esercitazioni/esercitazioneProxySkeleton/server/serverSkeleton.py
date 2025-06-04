from IMagazzino import IMagazzino
from skeletonThread import SkeletonThread
import socket

class ServerSkeleton(IMagazzino):
    def __init__(self, host, port, delegate):
        self.host = host
        self.port = port
        self.delegate = delegate

    def deposita(self, articolo, id):
       return self.delegate.deposita(articolo, id)
    

    def preleva(self, articolo):
        return self.delegate.preleva(articolo)


    def run_skeleton(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.host, self.port)
            
            print(f"[MAGAZZINO SKELETON] Server started on port: {s.getsockname()[1]}")

            s.listen(10)
            while True:
                conn, addr = s.accept()
                th = SkeletonThread(conn, self)
                th.start() ###sus
