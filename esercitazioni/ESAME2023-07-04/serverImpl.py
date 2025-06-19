from serverSkeleton import ServerSkeleton
import multiprocessing as mp

def produttore(ref, messaggioLog, tipo):
    message_to_put = f"{messaggioLog}-{tipo}"
    return ref.queue.put(message_to_put)


class ServerImpl(ServerSkeleton):

    def __init__(self, host, port):
        super().__init__(host, port)
        self.queue = mp.Queue(5)

    def log(self, messaggioLog, tipo):
        
        p = mp.Process(target=produttore, args=(self, messaggioLog, tipo))
        p.start()

        p.join()

    def consuma(self):
        return self.queue.get()
        
    