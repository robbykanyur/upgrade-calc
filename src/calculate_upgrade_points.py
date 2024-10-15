import os
from _constants import usac_points

def calculate_upgrade_points(conn):
  def calculate_usac_points (position, starters):
    try:
      position = int(position)
      starters = int(starters)
      if starters < 5:
        return 0
      for starter_range, points in usac_points.items():
        if starters in starter_range:
          return points.get(position, 0)
    except (ValueError, KeyError):
      return 0    
    return 0

  cursor = conn.cursor()
  cursor.execute("SELECT * FROM results ORDER BY race_date DESC")
  results = cursor.fetchall()

  update_data = []
  for i, result in enumerate(results):
    upgrade_points = calculate_usac_points(result[5], result[6])
    update_data.append((upgrade_points, result[0]))
  
  cursor.executemany("UPDATE results SET upgrade_points=? WHERE id=?", update_data)
  conn.commit()
