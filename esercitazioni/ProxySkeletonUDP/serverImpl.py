from threading import Lock, Condition
from IMagazzino import IMagazzino

import threading as mt

class serverImpl(IMagazzino):
    def __init__(self):
        self.max_size = 5
        self.laptop_queue = []
        self.smartphone_queue = []
        
        self.laptop_lock = Lock()
        self.cv_producer_laptop = Condition(self.laptop_lock)
        self.cv_consumer_laptop = Condition(self.laptop_lock)

        self.smartphone_lock = Lock()
        self.cv_producer_smartphone = Condition(self.smartphone_lock)
        self.cv_consumer_smartphone = Condition(self.smartphone_lock)


    def deposita(self, articolo, id):
        if articolo == "SMARTPHONE":
            with self.cv_producer_smartphone:
                self.cv_producer_smartphone.wait_for(lambda: self.theres_a_space(self.smartphone_queue))

                self.smartphone_queue.append(id)

                self.cv_consumer_smartphone.notify()
            
        else:
            with self.cv_producer_laptop:
                self.cv_producer_laptop.wait_for(lambda: self.theres_a_space(self.laptop_queue))

                self.laptop_queue.append(id)

                self.cv_consumer_laptop.notify()
        
        return "ACK"
    
    
    def preleva(self, articolo):
        if articolo == "SMARTPHONE":
            with self.cv_consumer_smartphone:
                self.cv_consumer_smartphone.wait_for(lambda: self.theres_an_item(self.smartphone_queue))

                removed_article = self.smartphone_queue.pop()


                with open("smartphone.txt", "a")as f:
                    f.write(removed_article)

                self.cv_producer_smartphone.notify()
        else:
            with self.cv_consumer_laptop:
                self.cv_consumer_laptop.wait_for(lambda: self.theres_an_item(self.laptop_queue))

                removed_article = self.laptop_queue.pop()


                with open("laptop.txt", "a")as f:
                    f.write(removed_article)

            self.cv_producer_laptop.notify()

        return removed_article

    def theres_a_space(self, queue):
        return len(queue) != 0

    def theres_an_item(self, queue):
        return len(queue) > 0