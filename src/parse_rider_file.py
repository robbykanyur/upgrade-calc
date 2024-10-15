import os
import sqlite3
from bs4 import BeautifulSoup
import re
from datetime import datetime
from dotenv import load_dotenv
from scrape_single_rider import scrape_single_rider

load_dotenv()

def extract_rider_details(text, pattern):
  match = re.search(pattern, text)
  return match.group(1) if match else None

def convert_to_number(text, default=999):
  try:
    return int(text)
  except(AttributeError, ValueError, TypeError):
    return default

def parse_race_date(race_day, race_month, race_year):
  race_date_str = f"{race_day} {race_month} {race_year}"
  return datetime.strptime(race_date_str, "%d %b %Y").strftime("%Y-%m-%d")

def process_rider_data():
  with sqlite3.connect(os.getenv('DB_PATH')) as conn:
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM riders")
    riders = cursor.fetchall()

    cursor.execute("SELECT date from completed_scrapes WHERE type='Riders' ORDER BY id DESC")
    most_recent_scrape_date = cursor.fetchone()[0]

    rider_update_data = []
    result_update_data = []

    for rider in riders:
      rider_id = rider[0]
      rider_file_path = f"./data/riders/{most_recent_scrape_date}/{rider_id}.txt"

      if not os.path.exists(rider_file_path):
        print(f"File not found for rider {rider_id}. Attempting to scrape")
        scrape_single_rider(rider_id, most_recent_scrape_date)

      with open(rider_file_path, "r") as file:
        print(f"Parsing file for rider {rider_id}")
        soup = BeautifulSoup(file.read(), "html.parser")
        rider_details = soup.select_one(".racerdetails").text
        raw_details = [extract_rider_details(rider_details, r"Racing Age:\s+(\d+)"), extract_rider_details(rider_details, r"Category:\s+(\d+)")]
        rider_age = convert_to_number(raw_details[0], default=999)
        rider_category = convert_to_number(raw_details[1], default=999)
        
        rider_update_data.append([rider_age, rider_category, rider_id])

        years = [re.search(r'(\d{4})', str(year)).group(1) for year in soup.find_all(class_="expandMonth")]
        race_history = soup.find_all(class_="monthContent")

        for i, racing_year in enumerate(race_history):
          race_rows = racing_year.select(".datatable1 tr.datarow1, tr.datarow2")
          for race in race_rows:
            race_data = race.select("td")
            race_date_parts = race_data[0].text.split()
            race_name = ' '.join(race_data[1].text.split())
            race_category = race_data[2].text
            race_position = race_data[4].text
            race_starters = race_data[5].text
            race_date = parse_race_date(race_date_parts[1], race_date_parts[0], years[i])

            if rider_age == 999:
              age_at_race = 999
            else:
              difference = datetime.now().year - int(years[i])
              age_at_race = rider_age - difference

            result_update_data.append([rider_id, race_date, race_name, race_category, race_position, race_starters, age_at_race])

    cursor.executemany("""
      UPDATE riders SET age = ?, current_category = ? WHERE id = ?
    """, (rider_update_data))

    cursor.executemany("""
      INSERT INTO results (rider_id, race_date, race_name, race_category, race_position, race_starters, age_at_race)
      VALUES (?, ?, ?, ?, ?, ?, ?)            
    """, result_update_data)

    conn.commit()

process_rider_data()