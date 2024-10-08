import sqlite3
conn = sqlite3.connect("./db/main.db")

sql_create_races_table = """ CREATE TABLE IF NOT EXISTS races(
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  date TEXT NOT NULL,
  crossresults_id TEXT NOT NULL
)"""

sql_create_riders_table = """ CREATE TABLE IF NOT EXISTS riders(
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  current_category TEXT,
  age
)"""

cursor = conn.cursor()
cursor.execute(sql_create_races_table)
cursor.execute(sql_create_riders_table)

races = [
  ["Jackson Park", "2023-10-07", "11821"],
  ["ABD Sunrise Park", "2023-10-22", "11934"],
  ["Campton CX", "2023-10-29", "11999"],
  ["Groundhog PSI", "2023-11-05", "12049"],
  ["Wheeling Heritage Park", "2023-11-12", "12100"],
  ["Quarry Cross", "2023-11-19", "12152"],
  ["Montrose Beach CX", "2023-12-03", "12211"],
  ["Glenwood Academy", "2024-09-29", "12471"]
]

def seed_races():
  for race in races:
    cursor.execute('''
      INSERT INTO races (id, name, date, crossresults_id)
      VALUES(?, ?, ?, ?)
  ''', (None, race[0], race[1], race[2])) 

# seed_races()

conn.commit()
cursor.close()
conn.close()