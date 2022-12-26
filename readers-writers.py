from threading import Thread, Condition, Lock
from time import sleep
from random import randint, choice
import string

text = ''

class Writer(Thread):

    TIMEOUT = (1, 3)
    SLEEP = (1, 2) 

    def __init__(self, name):
        super().__init__(name=name)
      
    def run(self):
        while True:
            global text
            with lock:
                text = ''
                print('Писатель {0} пишет книгу'.format(self.name))
                if not text:
                    for _ in range (5):
                        text += choice(string.ascii_letters)
                        sleep(randint(*Writer.TIMEOUT))
                        condition.acquire()
                        condition.notify_all()
                        condition.release()
                print('Писатель {0} закончил писать книгу {1}'.format(self.name, text))
            sleep(randint(*Writer.SLEEP))


class Reader(Thread):

    def __init__(self, name):
        super().__init__(name=name)

    def run(self):
        global text
        while True:
            with condition:
                condition.wait()
                print("Читатель {} читает: ".format(self.name), text)
       

if __name__ == "__main__":
    condition = Condition()
    lock = Lock()
    for nums in range(5): #кол-во писателей
        Writer(str(nums)).start()
    for nums in range(10):
            Reader(str(nums)).start() 
        
   