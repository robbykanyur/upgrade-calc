import sqlite3
import re

conn = sqlite3.connect('./db/main.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM results ORDER BY race_date DESC")
results = cursor.fetchall()

points = {
  "5-10": {
    1: 3,
    2: 2,
    3: 1
  },
  "11-20": {
    1: 4,
    2: 3,
    3: 2,
    4: 1
  },
  "21-35": {
    1: 5,
    2: 4,
    3: 3,
    4: 2,
    5: 1
  },
  "36-60": {
    1: 8,
    2: 6,
    3: 5,
    4: 4,
    5: 3,
    6: 2,
    7: 1
  },
  "61-80": {
    1: 10,
    2: 8,
    3: 7,
    4: 6,
    5: 5,
    6: 4,
    7: 3,
    8: 2,
    9: 1
  },
  "81+": {
    1: 11,
    2: 10,
    3: 9,
    4: 8,
    5: 7,
    6: 6,
    7: 5,
    8: 4,
    9: 3,
    10: 2,
    11: 1
  }
}

def calculate_upgrade_points (position, starters):
  try:
    position = eval(position)
    starters = eval(starters)
    if starters < 5:
      return 0
    elif starters >= 5 and starters <= 10:
      return points["5-10"][position]
    elif starters >= 11 and starters <= 20:
        return points["11-20"][position]
    elif starters >= 21 and starters <= 35:
        return points["21-35"][position]
    elif starters >= 36 and starters <= 60:
        return points["36-60"][position]
    elif starters >= 61 and starters <= 80:
        return points["61-80"][position]
    elif starters >= 81:
        return points["81+"][position]
  except:
    return 0

for i, result in enumerate(results):
  upgrade_points = calculate_upgrade_points(result[5], result[6])
  cursor.execute("UPDATE results SET upgrade_points=? WHERE id=?", (upgrade_points, result[0]))

conn.commit()
cursor.close()
conn.close()