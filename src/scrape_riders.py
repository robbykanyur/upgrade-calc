import os
from datetime import datetime
import requests
import sqlite3
from random import randint
from time import sleep

conn = sqlite3.connect('./db/main.db')
cursor = conn.cursor()

datestamp = datetime.now().strftime('%Y-%m-%d')

new_path = f'./data/riders/{datestamp}'
if not os.path.exists(new_path):
   os.makedirs(new_path)

def scrape_rider(rider_id):
  url = f'https://crossresults.com/racer/{rider_id}'
  req = requests.get(url)

  if req.status_code != 200:
      print(f'Failed to retrieve data for rider with id {rider_id}. Status code: {req.status_code}')
      return None
  
  with open(f"{new_path}/{rider_id}.txt", "w") as text_file:
     text_file.write(req.text)

cursor.execute('''
  SELECT * from riders
''')
riders = cursor.fetchall()
for rider in riders:
  if rider[0] <= 158055:
    print(f"Skipping rider with ID {rider[0]}")
  else:
    print(f"Scraping rider with ID {rider[0]}")
    scrape_rider(rider[0])
    
    sleep_interval = randint(5,15)
    print(f"Sleeping for {sleep_interval} seconds")
    sleep(sleep_interval)



