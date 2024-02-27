"""
Course: CSE 251 
Lesson: L07 Prove
File:   prove.py
Author: <Add name here>

Purpose: Process Task Files.

Instructions:

See Canvas for the full instructions for this assignment. You will need to complete the TODO comment
below before submitting this file:

TODO:

Add your comments here on the pool sizes that you used for your assignment and why they were the best choices.
"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 
import os

# Include cse 251 common Python files - Dont change
from cse251 import *

# Constants - Don't change
TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# TODO: Change the pool sizes and explain your reasoning in the header comment

PRIME_POOL_SIZE = 2
WORD_POOL_SIZE  = 4
UPPER_POOL_SIZE = 2
SUM_POOL_SIZE   = 2
NAME_POOL_SIZE  = 2

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []


def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
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


def task_prime(value):
    """
    Use the is_prime() above
    Return:
        {value} is prime
            - or -
        {value} is not prime
    """
    if is_prime(value):
        return f'{value} is prime'
    else:
        return f'{value} is not prime'

def task_word(word):
    """
    search in file 'words.txt'
    Return:
        {word} Found
            - or -
        {word} not found *****
    """
    if os.path.exists('words.txt'):
        with open('words.txt', 'r') as f:
            if word in f.read():
                return f'{word} Found'
            else:
                return f'{word} not found *****'
    else:
        return 'words.txt not found'

def task_upper(text):
    """
    Return:
        {text} ==>  uppercase version of {text}
    """
    return f'{text} ==> {text.upper()}'

def task_sum(start_value, end_value):
    """
    Return:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    total = sum(range(start_value, end_value + 1))
    return f'sum of {start_value:,} to {end_value:,} = {total:,}'

def task_name(url):
    """
    Return:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f'{url} has name {data["name"]}'
    else:
        return f'{url} had an error receiving the information'




def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # Create process pools
    prime_pool = mp.Pool(processes=PRIME_POOL_SIZE)
    word_pool = mp.Pool(processes=WORD_POOL_SIZE)
    upper_pool = mp.Pool(processes=UPPER_POOL_SIZE)
    sum_pool = mp.Pool(processes=SUM_POOL_SIZE)
    name_pool = mp.Pool(processes=NAME_POOL_SIZE)

    # Function to process each task type
    def process_task(task):
        task_type = task['task']
        if task_type == TYPE_PRIME:
            prime_pool.apply_async(task_prime, args=(task['value'],), callback= lambda x: result_primes.append(x))
        elif task_type == TYPE_WORD:
            word_pool.apply_async(task_word, args=(task['word'],), callback= lambda x: result_words.append(x))
        elif task_type == TYPE_UPPER:
            upper_pool.apply_async(task_upper, args=(task['text'],), callback= lambda x: result_upper.append(x))
        elif task_type == TYPE_SUM:
            sum_pool.apply_async(task_sum, args=(task['start'], task['end']), callback= lambda x: result_sums.append(x))
        elif task_type == TYPE_NAME:
            name_pool.apply_async(task_name, args=(task['url'],), callback= lambda x: result_names.append(x))
        else:
            log.write(f'Error: unknown task type {task_type}')

    # Load and process task files
    count = 0
    task_files = glob.glob("tasks/*.task")
    for filename in task_files:
        task = load_json_file(filename)
        count += 1
        process_task(task)

    # Close process pools and wait for all processes to finish
    prime_pool.close()
    word_pool.close()
    upper_pool.close()
    sum_pool.close()
    name_pool.close()

    prime_pool.join()
    word_pool.join()
    upper_pool.join()
    sum_pool.join()
    name_pool.join()


    # DO NOT change any code below this line!
    #---------------------------------------------------------------------------
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Total time to process {count} tasks')


if __name__ == '__main__':
    main()