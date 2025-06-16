from printerServerSkeleton import printerServerSkeleton
from multiprocessing import Queue

class ServerImpl(printerServerSkeleton):

    def __init__(self, host, port, queue=Queue(5)):
        super().__init__(host, port)
        self.queue = queue     

    def print(self, pathFile, tipo):
        print(f"[SERVER IMPL] Put in the internal queue the value: {pathFile}-{tipo}")
        return self.queue.put(f"{pathFile}-{tipo}")

    def consuma(self):
        print(f"[SERVER IMPL] Got a message from queue and sent it via stomp")
        return self.queue.get()