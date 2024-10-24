from _constants import excluded_not_elite, excluded_not_usac, category_mappings, excluded_events, excluded_exact_match, mixed_fields
from datetime import datetime

def identify_unique_categories(conn):
  cursor = conn.cursor()
  cursor.execute("SELECT race_date, race_name, race_category FROM results WHERE upgrade_points > 0 ORDER BY race_date DESC")
  results = cursor.fetchall()

  category_data = []
  new_categories = []
  cursor.execute("SELECT * FROM categories")
  existing_category_list = [category[2] for category in cursor.fetchall()]
    
  current_year = int(datetime.now().year)

  for result in results:
    race_date = result[0]
    race_name = result[1]
    original_category = result[2]

    if (int(race_date[:4]) >= (current_year - 1) and (race_name not in excluded_events) and (original_category not in existing_category_list) 
        and (original_category not in excluded_exact_match) and (original_category not in new_categories)):
      print(f"Adding new category to database: {original_category}")
      category_data.append((original_category, race_date))

  cursor.executemany("INSERT OR IGNORE INTO categories (category_name, race_date) VALUES (?, ?)", category_data)
  conn.commit()

  cursor.execute("SELECT category_name from categories")
  categories = cursor.fetchall()
  for category in categories:
    category_name = category[0]

    if any(x in category_name.upper() for x in excluded_not_elite):
      cursor.execute("UPDATE categories SET excluded=? WHERE category_name=?", (1, category_name))

    if any(x in category_name.upper() for x in excluded_not_usac):
      cursor.execute("UPDATE categories SET excluded=? WHERE category_name=?", (1, category_name))

    if category_name in mixed_fields:
      cursor.execute("UPDATE CATEGORIES SET excluded=?, mixed_field=? WHERE category_name=?", (0, 1, category_name))

  conn.commit()
  cursor.execute("SELECT category_name, mixed_field FROM categories WHERE excluded=0")
  categories = cursor.fetchall()

  for category in categories:
    category_name = category[0]
    mixed_field = category[1]
    if mixed_field == 1:
      simple_category = mixed_fields[category_name]
    else:
      simple_category = category_mappings[category_name]
    cursor.execute("UPDATE categories SET excluded=?, simple_category=? WHERE category_name=?", (0, simple_category, category_name))

  conn.commit()

