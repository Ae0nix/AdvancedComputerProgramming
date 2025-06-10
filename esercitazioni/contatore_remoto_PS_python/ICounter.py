from abc import ABC, abstractmethod

class ICounter(ABC):
    
    @abstractmethod
    def setCount(self, id, initial_value):
        pass

    @abstractmethod
    def sum(self, increment):
        pass

    @abstractmethod
    def increment(self):
        pass