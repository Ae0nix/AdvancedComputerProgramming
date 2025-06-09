from Interface import Interface
import multiprocessing as mp
import socket

def proc_func(conn, service):
    
    data = conn.recv(1024)

    if str(data.decode()) == "preleva":
        result = service.preleva()
    else:
        id = str(data.decode()).split('-')[1]
        result = service.deposita(id)

    conn.send(str(result).encode())

    conn.close()


class SkeletonServer(Interface):

    def __init__(self, queue):
        self.host = "localhost"
        self.port = 0

    def preleva(self):
        pass

    def deposita(self, id_articolo):
        pass
    
    def run_skeleton(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))

            print(f"[SERVER] Server is listening on port {s.getsockname()[1]}")
            s.listen(10)

            while True:
                conn, addr = s.accept()

                p = mp.Process(target=proc_func, args=(conn, self))
                p.start()
            

class ServerImpl(SkeletonServer):

    def deposita(self, id_articolo):
        self.queue.put(id_articolo)

        return "deposited"
    
    def preleva(self):
        result = self.queue.get()

        return result
    

if __name__ == "__main__":
    PORT = 0

    q = mp.Queue(5)

    serviceImpl = ServerImpl(q)
    serviceImpl.run_skeleton()
