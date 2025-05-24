from abc import ABC, abstractmethod

class DispatcherService(ABC):
    @abstractmethod
    def sendCmd(self, command):
        pass 

    @abstractmethod
    def getCmd(self):
        pass 
