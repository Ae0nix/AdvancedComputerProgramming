from Interface import Interface
import stomp
import socket
import sys

import multiprocessing as mp

class SkeletonProcess(mp.Process):

    def __init__(self, conn, proxy, msg):
        mp.Process.__init__(self)
        self.msg = msg
        self.proxy = proxy
        self.conn = conn


    def run(self):
        request = self.mess.split("-")[0]

        if request == "preleva":
            result = self.proxy.preleva()
        else:
            id = self.mess.split("-")[1]
            result = self.proxy.deposita(id)

        self.conn.send('/queue/response', result)



class DispatcherProxy(Interface):
    def __init__(self, port):
        self.port = port
        self.host = 'localhost'
        self.buf_size = 1024

    def deposita(self, id_articolo):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            message = f"deposita-{id_articolo}"
            s.send(message.encode("utf-8"))

            result = s.recv(self.buf_size)

            return result
    
    def preleva(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            message = "preleva"
            s.send(message.encode("utf-8"))

            data = s.recv(self.buf_size)

            return data


class MyListener(stomp.ConnectionListener):
    def __init__(self, conn, port):
        self.conn = conn
        self.port = port

    def on_message(self, frame):
        
        proxy = DispatcherProxy(self.port)

        p = SkeletonProcess(conn, proxy, frame.body)
        p.start()
        




if __name__ == "__main__":
    try:
        port = sys.argv[1]
    except IndexError:
        print("USAGE dispatcher.py [PORT]")

    conn = stomp.Connection('127.0.0.1', 61613)
    conn.set_listener('', MyListener(conn, port))
    conn.connect(wait=True)

    conn.subscribe(destination='/queue/requests', id = 1, ack='auto')