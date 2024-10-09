import os
import sqlite3
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import re
from datetime import datetime
from time import strptime, mktime

load_dotenv()
conn = sqlite3.connect('./db/main.db')
cursor = conn.cursor()

most_recent_rider_data = os.getenv('MOST_RECENT_RIDER_DATA')

cursor.execute("SELECT * FROM riders")
riders = cursor.fetchall()

for rider in riders:
  f = open(f"./data/riders/{most_recent_rider_data}/{rider[0]}.txt").read()
  soup = BeautifulSoup(f, "html.parser")

  rider_details = soup.select(".racerdetails")[0].text

  def extract_rider_details(text, pattern):
    match = re.search(pattern, text)
    return match.group(1) if match else None

  rider_age = extract_rider_details(rider_details, r"Racing Age:\s+(\d+)")
  rider_category = extract_rider_details(rider_details, r"Category:\s+(\d+)")
  cursor.execute("UPDATE riders SET current_category=?, age=? WHERE id=?", (rider_category, rider_age, rider[0]))
  print(f"Updating rider {rider[0]} ({rider[1]}) to Cat {rider_category} and age {rider_age}.")

  history = soup.find_all(class_="expandMonth")
  pattern = r'(\d{4})\s*.*'
  years = []
  for year in history:
    match = re.search(pattern, str(year))[1]
    years.append(match)

  race_history = soup.find_all(class_="monthContent")
  for i,racing_year in enumerate(race_history):
    table = racing_year.css.select(".datatable1 tr.datarow1,tr.datarow2")
    for race in table:
      race_data = race.css.select("td")
      race_date = race_data[0].contents[0].split()
      race_name = ' '.join(race_data[1].text.split())
      race_category = race_data[2].text
      race_position = race_data[4].text
      race_starters = race_data[5].text
      
      race_year = years[i]
      race_month = race_date[0]
      race_day = race_date[1]

      race_datestamp = datetime.fromtimestamp(mktime(strptime(f"{race_day} {race_month}, {race_year}", "%d %b, %Y")))
      race_date = race_datestamp.strftime("%Y-%m-%d")
      
      cursor.execute("SELECT * FROM results where rider_id=? AND race_date=? AND race_category=?", (rider[0], race_date, race_category))
      existing_record = cursor.fetchone()
  
      if not existing_record:
        cursor.execute("""INSERT INTO results (id, rider_id, race_date, race_name, race_category, race_position, race_starters, upgrade_points) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
                          (None, rider[0], race_date, race_name, race_category, race_position, race_starters, None))
        print(f"Added result from {race_name} on {race_date} for rider {rider[0]} to database.")
    
conn.commit()
cursor.close()
conn.close()