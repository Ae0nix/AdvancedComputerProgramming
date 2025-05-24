from abc import ABC, abstractmethod

class IMagazzino(ABC):

    @abstractmethod
    def deposita(self, articolo, id):
        raise NotImplementedError
    
    @abstractmethod
    def preleva(self, articolo):
        raise NotImplementedError
