import os
import sqlite3
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

most_recent_race_data = os.getenv('MOST_RECENT_RACE_DATA')

def insert_rider(cursor, racer_id, racer_name):
  cursor.execute('SELECT * FROM riders where id = ?', (racer_id,))
  racer_record = cursor.fetchone()

  if not racer_record:
    cursor.execute('''
      INSERT INTO riders (id, name)
      VALUES (?, ?)
    ''', (racer_id, racer_name))

def create_rider_list():
  with sqlite3.connect(os.getenv('DB_PATH')) as conn:
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM races')
    races = cursor.fetchall()

    cursor.execute("SELECT date FROM completed_scrapes WHERE type='Races' ORDER BY id DESC")
    most_recent_scrape_date = cursor.fetchone()[0]

    for race in races:
      race_id = race[3] # crossresults_id
      race_file_path = os.path.join('./data/races', most_recent_scrape_date, f"{race_id}.txt")

      if os.path.exists(race_file_path):
        with open(race_file_path, 'r') as f:
          soup = BeautifulSoup(f, "html.parser")

          for element in soup.find_all("tr", class_="resultsrow"):
            racer_id = element.get('id')[1:]
            racer_name_first = element.find_all('a')[1].contents[0].strip()
            racer_name_last = element.find_all('a')[2].contents[0].strip()
            racer_name = f"{racer_name_first} {racer_name_last}"

            insert_rider(cursor, racer_id, racer_name)
      else:
        print(f"Race file not found: {race_file_path}")

    conn.commit()