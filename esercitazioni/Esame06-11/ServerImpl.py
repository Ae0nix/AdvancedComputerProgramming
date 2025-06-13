from printerServerSkeleton import printerServerSkeleton
from multiprocessing import Queue

class ServerImpl(printerServerSkeleton):

    def __init__(self, queue=Queue(5)):
        self.queue = queue        

    def print(self, pathFile, tipo):
        return self.queue.put(f"{pathFile}-{tipo}")
