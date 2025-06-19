from abc import ABC, abstractmethod

class ILogging(ABC):
    @abstractmethod
    def log(self, messaggioLog, tipo):
        pass