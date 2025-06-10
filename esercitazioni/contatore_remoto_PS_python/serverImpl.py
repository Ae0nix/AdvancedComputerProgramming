from ICounter import ICounter
from multiprocessing import Lock

class serverImpl(ICounter):
    
    def __init__(self):
        self.counter = 0

        self.counterLock = Lock()

    def sum(self, increment):
        with self.counterLock:
            increment = int(increment)
            print(f"[SERVER] Il valore del counter è stato correttamente incrementato di {increment}")
            self.counter += increment
            return self.counter
    
    def increment(self):
        with self.counterLock:
            print("[SERVER] Il valore del counter è stato correttamente incrementato di 1")
            self.counter += 1
            return self.counter

    def setCount(self, id, initial_value):
        with self.counterLock:
            initial_value = int(initial_value)
            print(f"[SERVER] Il thread con id: {id} ha settato il valore del counter a {initial_value}")
            self.counter = initial_value
            return self.counter