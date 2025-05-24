from dispatcher_service import DispatcherService 
import multiprocessing as mq

class DispatcherImpl(DispatcherService):

    def __init__(self, queue=mq.Queue(5)):
        self.queue = queue

    def sendCmd(self, command):
        self.queue.put(command)

    def getCmd(self):
        return self.queue.get()

