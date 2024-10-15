import os
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count
from utilities import get_latest_scrape_dir

most_recent_race_data = os.getenv('MOST_RECENT_RACE_DATA')

def parse_race_file(args):
  race_file_path, race_id = args
  rider_list = []

  if os.path.exists(race_file_path):
    with open(race_file_path, 'r') as f:
      print(f"Parsing results for for race {race_id}")
      soup = BeautifulSoup(f, "lxml")

      for element in soup.find_all("tr", class_="resultsrow"):
        racer_id = element.get('id')[1:]
        racer_name_first = element.find_all('a')[1].contents[0].strip()
        racer_name_last = element.find_all('a')[2].contents[0].strip()
        racer_name = f"{racer_name_first} {racer_name_last}"

        rider_list.append((racer_id, racer_name))
  else:
    print(f"Race file not found: {race_file_path}")

  return rider_list

def create_rider_list(conn):
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM races')
  races = cursor.fetchall()

  most_recent_scrape_date = get_latest_scrape_dir('./data/races')
  rider_update_data = []

  race_file_paths = [(f"./data/races/{most_recent_scrape_date}/{race[3]}.txt", race[3]) for race in races]

  with Pool(cpu_count()) as pool:
    results = pool.map(parse_race_file, race_file_paths)

  for result in results:
    if result:
      rider_update_data.extend(result)

  cursor.executemany("""
    INSERT or REPLACE into riders (id, name)
    VALUES (?, ?)
  """, rider_update_data)

  conn.commit()