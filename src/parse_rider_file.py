import os
from bs4 import BeautifulSoup
import re
from datetime import datetime
from scrape_single_rider import scrape_single_rider
from multiprocessing import Pool, cpu_count
from utilities import get_latest_scrape_dir

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

def parse_rider_file(args):
  rider_file_path, rider_id, most_recent_scrape_date = args

  if not os.path.exists(rider_file_path):
      print(f"File not found for rider {rider_id}. Attempting to scrape")
      scrape_single_rider(rider_id, most_recent_scrape_date)

  if os.path.exists(rider_file_path):
    with open(rider_file_path, "r") as file:
      print(f"Parsing file for rider {rider_id}")
      soup = BeautifulSoup(file.read(), "lxml")
      rider_details = soup.select_one(".racerdetails").text
      raw_details = [extract_rider_details(rider_details, r"Racing Age:\s+(\d+)"), extract_rider_details(rider_details, r"Category:\s+(\d+)")]
      rider_age = convert_to_number(raw_details[0], default=999)
      rider_category = convert_to_number(raw_details[1], default=999)
      
      rider_update_data = [rider_age, rider_category, rider_id]
      result_update_data = []

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

  return [rider_update_data, result_update_data]

def process_rider_data(conn):
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM riders")
  riders = cursor.fetchall()

  most_recent_scrape_date = get_latest_scrape_dir("./data/riders")

  rider_update_data = []
  result_update_data = []
  rider_file_paths = [(f"./data/riders/{most_recent_scrape_date}/{rider[0]}.txt", rider[0], most_recent_scrape_date) for rider in riders]

  with Pool(cpu_count()) as pool:
    results = pool.map(parse_rider_file, rider_file_paths)

  for result in results:
    if result:
      rider_update_data.append(result[0])
      result_update_data.extend(result[1])

  cursor.executemany("""
    UPDATE riders SET age = ?, current_category = ? WHERE id = ?
  """, rider_update_data)

  cursor.executemany("""
    INSERT INTO results (rider_id, race_date, race_name, race_category, race_position, race_starters, age_at_race)
    VALUES (?, ?, ?, ?, ?, ?, ?)            
  """, result_update_data)

  conn.commit()