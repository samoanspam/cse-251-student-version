"""
Course: CSE 251 
Lesson: L01 Team Activity
File:   team.py
Author: Teia Patane

Purpose: Find prime numbers

Instructions:

- Don't include any other Python packages or modules
- Review and follow the team activity instructions (team.md)
"""

from datetime import datetime, timedelta
import threading
import random

# Include cse 251 common Python files
from cse251 import *


# Global variable for counting the number of primes found
prime_count = 0
numbers_processed = 0

def thread_function(start, range_count):
    global prime_count

    for i in range(start, start + range_count):
        if is_prime(i):
            prime_count += 1
            print(i, end=', ', flush=True)
    print(flush=True)


    # Should find 4306 primes

def is_prime(n):
    global numbers_processed
    numbers_processed += 1

    """
    Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """

    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


if __name__ == '__main__':
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO 1) Get this program running
    # TODO 2) move the following for loop into 1 thread
    # TODO 3) change the program to divide the for loop into 10 threads
    # TODO 4) change range_count to 100007.  Does your program still work?  Can you fix it?
    # Question: if the number of threads and range_count was random, would your program work?


    start = 10000000000
    range_count = 100000

    threads = []

    for i in range(10):
        i = threading.Thread(target= thread_function, args = (start, range_count))
        threads.append[i]


    for i in threads: 
        i.start()
    for i in threads:
        i.join()


    log.write(f'Numbers processed = {numbers_processed}')
    log.write(f'Primes found      = {prime_count}')
    log.stop_timer('Total time')




