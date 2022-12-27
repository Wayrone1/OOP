from multiprocessing import Process, Lock 
from time import sleep
from random import randint

PHILOSOPHERS = 6

class Philosophers(Process):
    EAT = 1, 2
    THINK = 3, 4
    TIMEOUT = 0.01
    
    def __init__(self, name, chopstickL, chopstickR):
        super().__init__(name=name)
        self.name, self.chopstickL, self.chopstickR  =  name, chopstickL, chopstickR
        
    def eat(self):
        print(f'Философ {self.name} начал есть')
        sleep(randint(*Philosophers.EAT))
        print(f'Философ {self.name} закончил есть и начал думать')

    def run(self):
        while True:
            if self.chopstickL.acquire(timeout=Philosophers.TIMEOUT): #запрашивает блокировку с таймаутом философа 
                if self.chopstickR.acquire(timeout=Philosophers.TIMEOUT):
                    print(f'Философ {self.name} взял левую палочку')
                    print(f'Философ {self.name} взял правую палочку')
                    self.eat()
                    self.chopstickL.release() #освобождает блокировку 
                    self.chopstickR.release()
                    sleep(randint(*Philosophers.THINK))
                    print(f'Философ {self.name} закончил думать и хочет есть')
                else:
                    self.chopstickL.release() #если он взял одну палку, но не взял другую, то он должел положить первую

if __name__ == "__main__":
    chopsticks = [Lock() for _ in range(PHILOSOPHERS)]
    for i in range(PHILOSOPHERS):
        chopL = chopsticks[i-1] 
        chopR = chopsticks[i] 
        Philosophers(str(i), chopL, chopR).start()


