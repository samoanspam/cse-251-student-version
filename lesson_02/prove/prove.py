"""
Course: CSE 251 
Lesson: L02 Prove
File:   prove.py
Author: <Add name here>

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py" and leave it running.
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the description of the assignment.
  Note that the names are sorted.
- You are required to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a separate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here

class Request_thread(threading.Thread):

  # This is the constructor being passed "self" and a url
  def __init__(self, url):
      threading.Thread.__init__(self)
      self.url = url
      self.respsone = {}
      self.status_code = {}

# This is the run funciton that runs when start is pressed, if a call is made to the internet the response
# will return a 200 if the connection works. It will also record the response to a .json file, or a "temporary" file.
  def run(self):
      response = requests.get(self.url)
      self.status_code = response.status_code

      if response.status_code == 200:
          self.respsone = response.json()
      else:
          print('Response = ', response.status_code)

# TODO Add any functions you need here
# A display funciton.
def display():
    print()

def retrieve_API(url):
    get = threading.Thread()

def filter_only_film6():
    for i in range(10):
        print()


def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # TODO Retrieve Top API urls
    retrieve_API()

    # TODO Retrieve Details on film 6
    filter_only_film6()

    # TODO Display results
    display()
    
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()