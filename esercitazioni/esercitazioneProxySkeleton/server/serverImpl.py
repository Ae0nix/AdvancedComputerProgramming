from IMagazzino import IMagazzino
from multiprocessing import Lock, Condition
from pymongo import MongoClient

class MagazzinoImpl(IMagazzino):

    def __init__(self, queue_size):
        self.laptop_queue = []
        self.smartphone_queue = []
        self.queue_size = queue_size
        self.client = MongoClient("localhost",27017)
        self.database = self.client["magazzino-db"]

        cv_laptop_lock = Lock()
        self.laptop_consumer_cv = Condition(lock=cv_laptop_lock)
        self.laptop_producer_cv = Condition(lock=cv_laptop_lock)

        cv_smartphone_lock = Lock()
        self.smartphone_consumer_cv = Condition(lock=cv_smartphone_lock)
        self.smartphone_producer_cv = Condition(lock=cv_smartphone_lock)

        self.laptop_collection = self.database["laptop"]
        self.smartphone_collection = self.database["smartphone"]
        
    def deposita(self, articolo, id):
        if articolo == "laptop":
            """
            acquisisco il lock e mi metto in attesa che ci sia spazio tramite quella funzione lambda
            wait_for vuole una funzione in input che restituisca True quando si può procedere altrimenti il thread aspetta
            """
            with self.laptop_producer_cv: ### acquisisco il lock associato alla cv
                self.laptop_producer_cv.wait_for(lambda: self.theres_a_space(self.laptop_queue)) ### metto il thread in attesa se il lock no è disponibile andando 

                self.laptop_queue.append(id)
                print(f"[IMPL] Added {id} in {articolo}")

                self.laptop_consumer_cv.notify()
        elif articolo == "smartphone":
            with self.smartphone_producer_cv:
                self.smartphone_producer_cv.wait_for(lambda: self.theres_a_space(self.smartphone_queue))

                self.smartphone_queue.append(id)
                print(f"[IMPL] Added {id} in {articolo}")
                
                self.smartphone_consumer_cv.notify()
        else:
            print("[MAGAZZINO IMPL] Articolo non riconosciuto")
            return "Failure"
        return "ACK"

    def preleva(self, articolo):
        if articolo == "laptop":
            with self.laptop_consumer_cv:
                self.laptop_consumer_cv.wait_for(lambda: self.thers_an_item(self.laptop_queue))

                id = self.laptop_queue.pop()
                print(f"[MAGAZZINO IMPL] Got {id} from {articolo}")

                ### parte di scrittura sul database
                self.laptop_collection.insert_one({"id": id})

                self.laptop_producer_cv.notify()

        elif articolo == "smartphone":
            with self.smartphone_consumer_cv:
                self.smartphone_consumer_cv.wait_for(lambda: self.thers_an_item(self.smartphone_queue))

                id = self.smartphone_queue.pop()
                print(f"[MAGAZZINO IMPL] Got {id} from {articolo}")

                self.smartphone_collection.insert_one({"id": id})

                self.smartphone_producer_cv.notify()

        else:
            print("[MAGAZZINO IMPL] Articolo non riconosciuto")
            return "Failure"
        
        return "ACK"

    def theres_a_space(self, queue):
        return len(queue) != self.queue_size
    
    def thers_an_item(self, queue):
        return len(queue) > 0
