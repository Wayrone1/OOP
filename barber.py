from time import sleep
from random import randint, choice
from multiprocessing import Process, Queue, Event

HAIRCUT = ['стрижку машинкой 1-2 насадки', 'стрижку модельную', 'стрижку фейд', 'стрижку кроп', 'стрижку андеркат', 'стрижку площадку']
NAME = ['Алексей', 'Кирилл', 'Витя', 'Максим228', 'Денис', 'Илья', 'Арсений', 'Никита']
QUEUE = 1
CUSTOMER_TIME  = (1, 2)
WAIT = 20

class Customer:
    def __init__(self, name, trim):
        self.name, self.trim = name, trim

class Barber:
    WORK_TIME = 10, 20
    def __init__(self, haircut):
        self.haircut = haircut
        self.customer_arrived = Event()
    
    def sleep(self):
        print('Парикмахер спит')
        return self.customer_arrived.wait(timeout=WAIT) #блокирует выполнение до тех пор, пока внутренний флаг не станет истинным True.
        
    def call(self):
        self.customer_arrived.set() #Пробуждаются все потоки, ожидающие его выполнения. 
    
    def work(self, customer: Customer):
        print(f'Парикмахер делает {customer.trim} которую выбрал {customer.name}')
        sleep(randint(*Barber.WORK_TIME))
        self.customer_arrived.clear() #Впоследствии потоки, вызывающие метод Event.wait(), будут блокироваться до тех пор, пока не будет вызван Event.set(), чтобы снова установить внутренний флаг в True.
        print(f'{customer.name} уходит')

class Barbershop:
    def __init__(self, haircut, queue: int):
        self.haircut, self.queue = haircut, queue
        self.worker = Barber(haircut)
        self.process = Process(target=self.work)
        self.que = Queue()

    def open(self):
        print(f'Салон открывается с {self.queue} местами в очереди')
        self.process.start()

    def close(self):
        print('Клиентов больше нет, парикмахер закрыл салон')

    def work(self):
        while True:
            if self.que.empty(): #возвращает новый массив заданной формы и типа без инициированных записей
                work_result = self.worker.sleep()
                if not work_result:
                    self.close()
                    break
            else:
                customer = self.que.get() #возвращает значение 
                self.worker.work(customer)

    def visit(self, customer: Customer):
        print(f'{customer.name} зашел в салон и ищет место в записи')
        if not self.que.full():
                print(f'Зал ожидания заполнен, {customer.name} уходит')
        else:        
            print(f'{customer.name} выбрал {customer.trim}')
            self.que.put(customer) #входит в очередь
            self.worker.call() #парикмахер забирает его из очереди 

if __name__ == '__main__':
    names = [str(i) for i in range(10)]
    customers = [Customer(choice(NAME), choice(HAIRCUT)) for _ in names]
    barber_shop = Barbershop(HAIRCUT, QUEUE)
    barber_shop.open()
    for customer in customers:
        sleep(randint(*CUSTOMER_TIME))
        barber_shop.visit(customer) #Вот отсюда идет на 47-56 и если очередь полная то 61, 64 он в очереди