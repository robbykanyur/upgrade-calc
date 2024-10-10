import sqlite3
from datetime import datetime, timedelta
from time import strftime
import re

conn = sqlite3.connect('./db/main.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM riders")
results = cursor.fetchall()

points = {}

for rider in results:
  points[rider[0]] = {
    "upgrade_points": [],
    "cat_5_finishes": 0,
    "qualified_victories": 0,
  }

cursor.execute("SELECT * FROM results ORDER BY race_date asc")
results = cursor.fetchall()

for result in results:
  if "RELAY" in result[3].upper():
    continue

  cursor.execute("SELECT * FROM categories WHERE category_name=?", (result[4],))
  simple_category = cursor.fetchone()[3]

  cursor.execute("SELECT * FROM riders WHERE id=?", (result[1],))
  rider_category = cursor.fetchone()[2]
  if not rider_category:
    rider_category = "0"

  race_date = datetime.strptime(result[2], "%Y-%m-%d")
  result_position = result[5]
  result_starters = result[6]
  match = re.search(r'\b(DNF|DNP|DQ)\b', result_position)
  
  if not match and simple_category:
    if (rider_category in simple_category) or "0" in simple_category:
      if "5" in simple_category and rider_category == "5" or rider_category == "0":
        points[result[1]]["cat_5_finishes"] += 1

      if simple_category and (rider_category in simple_category) and eval(result_position) == 1 and eval(result_starters) >= 20:
        points[result[1]]["qualified_victories"] += 1

      if race_date > (datetime.now() - timedelta(366)) and result[7] > 0:
        points[result[1]]["upgrade_points"].append(result[7])

for rider in points.items():
  rider_id = rider[0]
  upgrade_points = sum(rider[1]["upgrade_points"])
  cat_5_finishes = rider[1]["cat_5_finishes"]
  qualified_wins = rider[1]["qualified_victories"]
  datestamp = strftime("%Y-%m-%d")
  cursor.execute("""REPLACE INTO upgrade_points (rider_id, date_calculated, upgrade_points, cat_5_races, qualified_wins) values (?, ?, ?, ?, ?)""", 
                 (rider_id, datestamp, upgrade_points, cat_5_finishes, qualified_wins))

conn.commit()
cursor.close()
conn.close()