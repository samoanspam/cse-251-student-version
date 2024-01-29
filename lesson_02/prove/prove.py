# I wrote out what I could but I couldn't test it due to problems I had while trying to run the server.py file. I spoke with Brother Comeau a bit but I'll have to try to find
# time to come in so that I can try to solve whatever problem I'm having... I also don't have the display set out correclty.
"""
Course: CSE 251 
Lesson: L02 Prove
File:   prove.py
Author: Teia Patane

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
from cse251 import *

# Include cse 251 common Python files

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0
call_count_lock = threading.Lock()


# TODO Add your threaded class definition here

class Request_thread(threading.Thread):

  # This is the constructor being passed "self" and a url
  def __init__(self, url, category):
      threading.Thread.__init__(self)
      self.url = url
      self.category = category
      self.response = {}
      self.status_code = {}

# This is the run funciton that runs when start is pressed, if a call is made to the internet the response
# will return a 200 if the connection works. It will also record the response to a .json file, or a "temporary" file.
  def run(self):
      global call_count
      response = requests.get(self.url)
      self.status_code = response.status_code

      # incrementing call_count
      with call_count_lock:
          call_count += 1

      if response.status_code == 200:
          self.respsone = response.json()
      else:
          print(f'Response for {self.category} = ', response.status_code)

# TODO Add any functions you need here
# A display funciton.
def display(data):
    print('Displaying Results:')
    print()
    # prints all data written to json file and uses indent to make it look "nice"
    if isinstance(data, list):
        # If it's a list, print elements without curly brackets
        for item in data:
            print(item)
    else:
        # Otherwise, print JSON with indent
        print(json.dumps(data, indent=2))


def retrieve_category_data(category_url, category_name):
    # created a thread that runs the call
    thread = Request_thread(category_url, category_name)
    # starts and joins the thread
    thread.start()
    thread.join()

    return thread.response

# def filter_only_film6(film_url):
#     # creating a variable that runs the call
#     film_details = retrieve_category_data(film_url)
#     # prints out the information in the variable
#     print('Film 6 Details: ', film_details)


def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # TODO Retrieve Top API urls
    top_api_urls = retrieve_category_data(TOP_API_URL, 'Top API URLs')

    # TODO Retrieve Details on film 6
    # film_url = top_api_urls.get('films')
    # filter_only_film6(film_url)

    # a list to iterate through when grabbing different pieces of info
    categories = ['people', 'planets', 'species', 'vehicles', 'starships']
    category_data = {}

    for category in categories:
        category_url = top_api_urls.get(category)
        category_data[category] = retrieve_category_data(category_url, category)

    # TODO Display results
    # I know I have to format the data in a certain way but without being able to test it this is as far as I feel I can get.
    display(top_api_urls)

    for category, data in category_data.items():
        display({category: data})

    # TODO Display results
    # display(top_api_urls)
    
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
