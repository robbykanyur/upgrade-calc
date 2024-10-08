import sqlite3
from bs4 import BeautifulSoup
import soupsieve as sv

conn = sqlite3.connect('./db/main.db')
cursor = conn.cursor()

most_recent_race_data = "2024-10-07"

def create_rider_list():
 
  cursor.execute('SELECT * FROM races')
  races = cursor.fetchall()

  for race in races:
    f = open(f"./data/races/{most_recent_race_data}/{race[3]}.txt").read()
    soup = BeautifulSoup(f, "html.parser")
    for element in soup.find_all("tr", class_="resultsrow"):
      racer_id = element.get('id')[1:]
      racer_name_first = element.findAll('a')[1].contents[0].split()[0]
      racer_name_last = element.findAll('a')[2].contents[0].split()[0]
      
      racer_name = f"{racer_name_first} {racer_name_last}"
      cursor.execute('''SELECT * FROM riders where id = ?''', (racer_id,))
      racer_record = cursor.fetchone()
      
      if(not racer_record):
        cursor.execute('''
          INSERT INTO riders (id, name)
          VALUES (?, ?)             
        ''', (racer_id, racer_name))

        print(f"{racer_name} ({racer_id}) inserted into database")

  conn.commit()
  cursor.close()
  conn.close()

create_rider_list()