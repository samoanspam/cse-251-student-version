import time
import threading
import random
from cse251 import *

# Global Constants - DO NOT CHANGE
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has was just created in the terminal
        # print(f'Created: {self.info()}')
           
    def info(self):
        """ Helper function to quickly get the car information. """
        return f'{self.make} {self.model}, {self.year}'


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        assert len(self.items) <= 10
        self.items.append(item)

    def get(self):
        return self.items.pop(0)

class Factory(threading.Thread):
    def __init__(self, queue, produce_semaphore, consume_semaphore):
        threading.Thread.__init__(self)
        self.queue = queue
        self.produce_semaphore = produce_semaphore
        self.consume_semaphore = consume_semaphore

    def run(self):
        for i in range(CARS_TO_PRODUCE):
            car = Car()

            # Acquire the produce_semaphore to check if the queue is at its maximum size
            self.produce_semaphore.acquire()

            # Check if the queue is at its maximum size before putting the car
            while self.queue.size() >= MAX_QUEUE_SIZE:
                time.sleep(0.1)  # adjustable sleep time

            self.queue.put(car)
            print(f'Factory created: {car.info()}')

            # Release the consume_semaphore to indicate that a new car is available
            self.consume_semaphore.release()

        # Signal the dealer that there are no more cars
        final_car = "No more cars"
        self.queue.put(final_car)

        # Release the consume_semaphore to ensure the dealer can exit
        self.consume_semaphore.release()


class Dealer(threading.Thread):
    def __init__(self, queue, produce_semaphore, consume_semaphore, queue_stats, queue_stats_lock):
        threading.Thread.__init__(self)
        self.queue = queue
        self.produce_semaphore = produce_semaphore
        self.consume_semaphore = consume_semaphore
        self.queue_stats = queue_stats
        self.queue_stats_lock = queue_stats_lock

    def run(self):
        for i in range(CARS_TO_PRODUCE):
            # Acquire the consume_semaphore to check if a car is available in the queue
            self.consume_semaphore.acquire()

            car = self.queue.get()

            if car == "No more cars":
                print("There are no more cars to sell. Exiting.")
                break

            print(f'Dealership sold: {car.info()}')

            # Update queue_stats when the dealer receives a car
            with self.queue_stats_lock:
                self.queue_stats[self.queue.size()] += 1

            # Release the produce_semaphore to indicate that the queue has space for a new car
            self.produce_semaphore.release()

            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))


def main():
    log = Log(show_terminal=True)

    log.start_timer()
    
    produce_semaphore = threading.Semaphore(MAX_QUEUE_SIZE)
    consume_semaphore = threading.Semaphore(0)
    queue = Queue251()

    queue_stats_lock = threading.Lock()
    queue_stats = [0] * MAX_QUEUE_SIZE

    factory = Factory(queue, produce_semaphore, consume_semaphore)
    dealer = Dealer(queue, produce_semaphore, consume_semaphore, queue_stats, queue_stats_lock)

    factory.start()
    dealer.start()

    factory.join()
    dealer.join()

    log.stop_timer(f'All {CARS_TO_PRODUCE} cars have been created. ')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count', filename='Production Count vs Queue Size.png')


if __name__ == '__main__':
    main()