import os
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import sqlite3
import json
from random import randint
from time import sleep

conn = sqlite3.connect('./db/main.db')
cursor = conn.cursor()

datestamp = datetime.now().strftime('%Y-%m-%d')

new_path = f'./data/races/{datestamp}'
if not os.path.exists(new_path):
   os.makedirs(new_path)

def scrape_race(race_id):
  url = f'https://crossresults.com/race/{race_id}'
  req = requests.get(url)

  if req.status_code != 200:
      print(f'Failed to retrieve data for race with id {race_id}. Status code: {req.status_code}')
      return None
  
  with open(f"{new_path}/{race_id}.txt", "w") as text_file:
     text_file.write(req.text)

cursor.execute('''
  SELECT * from races
''')
races = cursor.fetchall()
for race in races:
  print(f"Scraping race with ID {race[3]}")
  scrape_race(race[3])
   
  sleep_interval = randint(5,15)
  print(f"Sleeping for {sleep_interval} seconds")
  sleep(sleep_interval)



