import os
from datetime import datetime
import requests
from requests.exceptions import RequestException
import sqlite3
from pathlib import Path
from random import randint
from time import sleep
from dotenv import load_dotenv
load_dotenv()

datestamp = datetime.now().strftime('%Y-%m-%d')
data_dir = Path(f"./data/races/{datestamp}")
data_dir.mkdir(parents=True, exist_ok=True)

new_path = f'./data/races/{datestamp}'
if not os.path.exists(new_path):
   os.makedirs(new_path)

def scrape_race(race_id, save_path):
  url = f'https://crossresults.com/race/{race_id}'
  
  max_retries = 3
  retry_count = 0
  while retry_count < max_retries:
    try:
      response = requests.get(url, timeout=10)
      if response.status_code == 200:
        race_file = save_path / f"{race_id}.txt"
        race_file.write_text(response.text)
        print(f"Successfully scraped race {race_id} and saved to file")
        return True
      else:
        print(f"Failed to scrape race {race_id}. Status code: {response.status_code}")
        return False
    except RequestException as e:
      retry_count += 1
      print(f"Error while scraping race {race_id}: {e}. Sleeping for 30 seconds and retrying ({retry_count}/{max_retries})")
      sleep(30)
  print(f"Failed to scrape race {race_id} after {max_retries} retries")
  return False

def fetch_races(conn):
  cursor = conn.cursor()
  cursor.execute('SELECT id, name, date, crossresults_id FROM races')
  races = cursor.fetchall()
  return races

def run_scraper():
  conn = sqlite3.connect(os.getenv('DB_PATH'))
  with conn:
    races = fetch_races(conn)
    for race in races:
      race_id = race[3] # crossresults_id
      scrape_race(race_id, data_dir)
      sleep_interval = randint(4,11)
      print(f"Sleeping for {sleep_interval} seconds before the next request")
      sleep(sleep_interval)
  conn.commit()
  conn.close()


