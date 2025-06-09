from abc import ABC, abstractmethod

class Interface(ABC):

    @abstractmethod
    def preleva(self):
        pass
    
    @abstractmethod
    def deposita(self, id_articolo):
        pass