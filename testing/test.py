# What are passed as value?: string, integer, float, bool
# What are passed as references?: list, dict, set, objects.

import threading
import time

class Display_Hello(threading.Thread):
    def __init__(self, number):
        # this is the consturctor
        threading.Thread.__init__(self)

        # this is where you creawte variables
        self.number = number

    def run(self):
        time.sleep(self.number)
        print(f'Hello World: {self.number}')


if __name__ == '__main__':
    hello1 = Display_Hello(2)
    hello2 = Display_Hello(1)

    hello1.start()
    hello2.start()

    hello1.join()
    hello2.join()