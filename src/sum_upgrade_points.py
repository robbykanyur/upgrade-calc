from datetime import datetime, timedelta
from time import strftime
import re

def sum_upgrade_points(conn):
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM riders")
  riders = cursor.fetchall()

  update_data = []
  datestamp = strftime("%Y-%m-%d")
  
  for rider in riders:
    rider_id = rider[0]
    rider_category = rider[2]
    data = {
      "rider_id": rider_id,
      "upgrade_points": 0,
      "cat_5_finishes": 0,
      "qualified_victories": 0,
    }

    cursor.execute("SELECT * FROM results WHERE rider_id=? ORDER BY race_date ASC", ((rider_id, )))
    results = cursor.fetchall()

    for result in results:
      race_position = result[5]
      race_starters = result[6]
      upgrade_points = result[8]
      race_date = datetime.strptime(result[2], "%Y-%m-%d")
      non_numerical_result = re.search(r'\b(DNF|DNP|DQ)\b', race_position)

      if (not non_numerical_result):
        if int(rider_category) >= 5:
          data["cat_5_finishes"] += 1
        if int(race_position) == 1 and int(race_starters) >= 20:
          data["qualified_victories"] += 1
        if race_date > (datetime.now() - timedelta(days = 366)) and upgrade_points > 0:
          data["upgrade_points"] += upgrade_points

    if data["cat_5_finishes"] != 0 or data["qualified_victories"] != 0 or data["upgrade_points"] != 0:
      update_data.append((data["rider_id"], datestamp, data["upgrade_points"], data["cat_5_finishes"], data["qualified_victories"]))

  cursor.executemany("""REPLACE INTO upgrade_points (rider_id, date_calculated, upgrade_points, cat_5_races, qualified_wins) values (?, ?, ?, ?, ?)""", 
                    (update_data))

  conn.commit()