import sqlite3
from datetime import datetime

conn = sqlite3.connect('./db/main.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM upgrade_points")
records = cursor.fetchall()

def insert_or_update_record(cursor, rider_id, datestamp, reason, details, warning):
  cursor.execute("""
        INSERT INTO upgrade_flags (rider_id, date_calculated, reason, details, warning)
        SELECT ?, ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM upgrade_flags WHERE rider_id = ? AND reason = ?
        )
        """, (rider_id, datestamp, reason, details, warning, rider_id, reason))

  cursor.execute("""UPDATE upgrade_flags SET date_calculated=?, details=? WHERE rider_id=? AND reason=?""",
                (datestamp, details, rider_id, reason))

for record in records:
  cursor.execute("SELECT * FROM riders where id=?", (record[1],))
  rider = cursor.fetchone()

  cursor.execute("SELECT * FROM results where rider_id=?", (rider[0],))
  results = cursor.fetchall()

  raced_this_season = False
  for result in results:
    if "2024" in result[2] and "Glenwood" in result[3]:
      raced_this_season = True
      break 

  datestamp = datetime.now().strftime('%Y-%m-%d')
  rider_category = rider[2]
  rider_age = rider[3]
  upgrade_points = record[3]
  cat_5_races = record[4]
  qualified_wins = record[5]
  warning = None

  if not rider_category:
    rider_category = "6"

  if not raced_this_season:
    warning = "Hasn't raced this season"
  elif rider_age:
    if eval(rider_age) < 23:
      warning = f"RIDER AGE {rider_age}"

  if eval(rider_category) >= 5:
    if upgrade_points >= 10:
      reason = "Too many Cat 5 points"
      details = f"{upgrade_points} (maximum 10)"
      insert_or_update_record(cursor, rider[0], datestamp, reason, details, warning)
    if cat_5_races >= 10:
      reason = "Too many Cat 5 races"
      details = f"{cat_5_races} races (maximum 10)"
      insert_or_update_record(cursor, rider[0], datestamp, reason, details, warning)
    if qualified_wins >= 2:
      reason = "Too many Cat 5 wins"
      details = f"{qualified_wins} wins (maximum 2)"
      insert_or_update_record(cursor, rider[0], datestamp, reason, details, warning)
  
  if eval(rider_category) == 4:
    if upgrade_points >= 10:
      reason = "Too many Cat 4 points"
      details = f"{upgrade_points} (maximum 10)"
      insert_or_update_record(cursor, rider[0], datestamp, reason, details, warning)
    if qualified_wins >= 2:
      reason = "Too many Cat 4 wins"
      details = f"{qualified_wins} wins (maximum 2)"
      insert_or_update_record(cursor, rider[0], datestamp, reason, details, warning)

  if eval(rider_category) == 3:
    if upgrade_points >= 15:
      reason = "Too many Cat 3 points"
      details = f"{upgrade_points} (maximum 15)"
      insert_or_update_record(cursor, rider[0], datestamp, reason, details, warning)
    if qualified_wins >= 2:
      reason = "Too many Cat 3 wins"
      details = f"{qualified_wins} wins (maximum 2)"
      insert_or_update_record(cursor, rider[0], datestamp, reason, details, warning)

  if eval(rider_category) == 2:
    if upgrade_points >= 20:
      reason = "Too many Cat 2 points"
      details = f"{upgrade_points} (maximum 15)"
      insert_or_update_record(cursor, rider[0], datestamp, reason, details, warning)
    if qualified_wins >= 2:
      reason = "Too many Cat 2 wins"
      details = f"{qualified_wins} wins (maximum 2)"
      insert_or_update_record(cursor, rider[0], datestamp, reason, details, warning)

# cursor.execute("DROP TABLE upgrade_flags")

conn.commit()
cursor.close()
conn.close()