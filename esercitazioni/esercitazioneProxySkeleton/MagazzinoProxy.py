from IMagazzino import IMagazzino

class MagazzinoProxy(IMagazzino):
    def __init__(self, host, port):
        self.host = host
        self.port = port


    def deposita(self, articolo, id):
        pass
    
    def preleva(self, articolo):
        pass