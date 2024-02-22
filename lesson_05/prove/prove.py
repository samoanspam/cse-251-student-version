
"""
Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread/process pools are not allowed
- You MUST use a barrier!
- Do not use try...except statements.
- You are not allowed to use the normal Python Queue object. You must use Queue251.
- The shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE.
"""

from datetime import datetime, timedelta
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Constants.
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru',
                 'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus',
                 'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE', 'Super', 'Tall', 'Flat', 'Middle', 'Round',
                  'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                  'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

    def info(self):
        return f'{self.make} {self.model}, {self.year}'


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, car_queue, semaphore):
        super().__init__()
        self.car_queue = car_queue
        self.semaphore = semaphore
        self.cars_to_produce = random.randint(200, 300)

    def run(self):
        for _ in range(self.cars_to_produce):
            car = Car()
            self.semaphore.acquire()
            self.car_queue.put(car)
            self.semaphore.release()


class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, car_queue, semaphore):
        super().__init__()
        self.car_queue = car_queue
        self.semaphore = semaphore
        self.cars_sold = 0

    def run(self):
        while True:
            self.semaphore.acquire()
            if len(self.car_queue.items) > 0:
                car = self.car_queue.get()
                car.cars_sold += 1
            else:
                self.semaphore.release()
                break
            self.semaphore.release()
            # Process the car (e.g., sell it)


def run_production(factory_count, dealer_count):
    """ This function will do a production run with the number of
        factories and dealerships passed in as arguments.
    """

    car_queue = Queue251()
    semaphore = threading.Semaphore(MAX_QUEUE_SIZE)
    factories = [Factory(car_queue, semaphore) for _ in range(factory_count)]
    dealers = [Dealer(car_queue, semaphore) for _ in range(dealer_count)]

    start_time = time.time()

    for factory in factories:
        factory.start()

    for dealer in dealers:
        dealer.start()

    for factory in factories:
        factory.join()

    end_time = time.time()

    for dealer in dealers:
        dealer.join()

    run_time = end_time - start_time

    return run_time, car_queue.max_size, [dealer.cars_sold for dealer in dealers], [factory.cars_to_produce for factory in factories]


def main(log):
    """ Main function - DO NOT CHANGE! """

    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for factories, dealerships in runs:
        run_time, max_queue_size, dealer_stats, factory_stats = run_production(factories, dealerships)

        log.write(f'Factories      : {factories}')
        log.write(f'Dealerships    : {dealerships}')
        log.write(f'Run Time       : {run_time:.4f}')
        log.write(f'Max queue size : {max_queue_size}')
        log.write(f'Factory Stats  : Made = {sum(factory_stats)} @ {factory_stats}')
        log.write(f'Dealer Stats   : Sold = {sum(dealer_stats)} @ {dealer_stats}')
        log.write('')

        # The number of cars produces needs to match the cars sold
        # assert sum(dealer_stats) == sum(factory_stats)


if __name__ == '__main__':
    log = Log(show_terminal=True)
    main(log)
