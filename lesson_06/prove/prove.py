"""
Course: CSE 251 
Lesson: L06 Prove
File:   prove.py
Author: Teia Patane

Purpose: Processing Plant

Instructions:

- Implement the necessary classes to allow gifts to be created.
"""
import random
import multiprocessing as mp
import os.path
import time
import datetime
import json

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.json'
BOXES_FILENAME   = 'boxes.txt'

# Settings constants
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
NUMBER_OF_MARBLES_IN_A_BAG = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

class Bag():
    """ Bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """
    Gift of a large marble and a bag of marbles - Don't change

    Parameters:
        large_marble (string): The name of the large marble for this gift.
        marbles (Bag): A completed bag of small marbles for this gift.
    """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'

class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, bagger_pipe, settings):
        mp.Process.__init__(self)
        self.bagger_pipe = bagger_pipe
        self.settings = settings

    def run(self):
        creator_delay = self.settings[CREATOR_DELAY]
        marble_count = self.settings[MARBLE_COUNT]

        for _ in range(marble_count):
            marble = random.choice(self.colors)
            self.bagger_pipe.send(marble)
            time.sleep(creator_delay)

        self.bagger_pipe.send(None)


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, creator_pipe, assembler_pipe, settings):
        mp.Process.__init__(self)
        self.creator_pipe = creator_pipe
        self.assembler_pipe = assembler_pipe
        self.settings = settings

    def run(self):
        bagger_delay = self.settings[BAGGER_DELAY]
        bag_size = self.settings[NUMBER_OF_MARBLES_IN_A_BAG]
        marbles = []

        while True:
            marble = self.creator_pipe.recv()
            if marble is None:
                break
            marbles.append(marble)
            if len(marbles) == bag_size:
                bag = Bag()
                for m in marbles:
                    bag.add(m)
                self.assembler_pipe.send(bag)
                marbles = []
            time.sleep(bagger_delay)

        self.assembler_pipe.send(None)


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, bagger_pipe, wrapper_pipe, settings):
        mp.Process.__init__(self)
        self.bagger_pipe = bagger_pipe
        self.wrapper_pipe = wrapper_pipe
        self.settings = settings

    def run(self):
        assembler_delay = self.settings[ASSEMBLER_DELAY]

        while True:
            bag = self.bagger_pipe.recv()
            if bag is None:
                break
            large_marble = random.choice(self.marble_names)
            gift = Gift(large_marble, bag)
            self.wrapper_pipe.send(gift)
            time.sleep(assembler_delay)

        self.wrapper_pipe.send(None)


class Wrapper(mp.Process):
    """ Takes created gifts and "wraps" them by placing them in the boxes file. """
    def __init__(self, assembler_pipe, gift_count, settings):
        mp.Process.__init__(self)
        self.assembler_pipe = assembler_pipe
        self.gift_count = gift_count
        self.settings = settings

    def run(self):
        wrapper_delay = self.settings[WRAPPER_DELAY]

        with open(BOXES_FILENAME, 'a') as boxes_file:
            while True:
                gift = self.assembler_pipe.recv()
                if gift is None:
                    break
                boxes_file.write(f'{datetime.now()}: {gift}\n')
                self.gift_count.value += 1
                time.sleep(wrapper_delay)

        self.gift_count.value += 1


def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')


def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    with open(CONTROL_FILENAME) as json_file:
        settings = json.load(json_file)

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}') 
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')

    # Create Pipes between creator -> bagger -> assembler -> wrapper
    creator_bagger_pipe = mp.Pipe()
    bagger_assembler_pipe = mp.Pipe()
    assembler_wrapper_pipe = mp.Pipe()

    # Create a variable to count the number of gifts
    gift_count = mp.Value('i', 0)

    # Delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # Create the processes
    marble_creator = Marble_Creator(creator_bagger_pipe[1], settings)
    bagger = Bagger(creator_bagger_pipe[0], bagger_assembler_pipe[1], settings)
    assembler = Assembler(bagger_assembler_pipe[0], assembler_wrapper_pipe[1], settings)
    wrapper = Wrapper(assembler_wrapper_pipe[0], gift_count, settings)

    log.write('Starting the processes')
    marble_creator.start()
    bagger.start()
    assembler.start()
    wrapper.start()

    log.write('Waiting for processes to finish')
    marble_creator.join()
    bagger.join()
    assembler.join()
    wrapper.join()

    display_final_boxes(BOXES_FILENAME, log)
    
    # Log the number of gifts created
    log.write(f'Number of gifts created: {gift_count.value}')

    log.stop_timer(f'Total time')

if __name__ == '__main__':
    main()
