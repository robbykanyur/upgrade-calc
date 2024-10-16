import os
from datetime import datetime
import requests
from requests.exceptions import RequestException
from random import randint
from time import sleep
from pathlib import Path

def scrape_rider(rider_id, save_path):
  url = f'https://crossresults.com/racer/{rider_id}'
  file_path = save_path / f"{rider_id}.txt"
  file_exists = os.path.isfile(file_path)

  max_retries = 3
  retry_count = 0
  while retry_count < max_retries:
    if file_exists:
       print(f"Rider {rider_id} has already been scraped")
       return False
    else:
      try:
        print(f"Scraping rider with ID {rider_id}")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            file_path.write_text(response.text)
            print(f"Successfully scraped rider {rider_id} and saved to file")
            return True
        else:
            print(f"Failed to scrape rider {rider_id}. Status code: {response.status_code}")
            return False
      except RequestException as e:
        retry_count += 1
        print(f"Error while scraping rider {rider_id}: {e}. Sleeping for longer and retrying ({retry_count}/{max_retries})")
        sleep(randint(30,60))
    print(f"Failed to scrape rider {rider_id} after {max_retries} retries")
    return False

def run_rider_scraper(conn):
  datestamp = datetime.now().strftime('%Y-%m-%d')
  data_dir = Path(f'./data/riders/{datestamp}')
  if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    
  cursor = conn.cursor()
  cursor.execute('SELECT id from riders')
  riders = cursor.fetchall()
  for rider in riders:
    rider_id = rider[0]
    scraped_successfully = scrape_rider(rider_id, data_dir)
    sleep_interval = randint(4,11)
    if scraped_successfully:
      print(f"Sleeping for {sleep_interval} seconds before next request")
      sleep(sleep_interval)

