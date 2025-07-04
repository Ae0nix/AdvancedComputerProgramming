from abc import abstractmethod, ABC

class IMagazzino(ABC):

    @abstractmethod
    def deposita(self, articolo, id):
        pass
    
    @abstractmethod
    def preleva(self, articolo):
        pass