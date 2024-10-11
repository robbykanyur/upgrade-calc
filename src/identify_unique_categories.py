import sqlite3
from _constants import excluded_not_elite, excluded_not_usac

conn = sqlite3.connect('./db/main.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM results ORDER BY race_date DESC")
results = cursor.fetchall()

for result in results:
  race_date = result[2]
  original_category = result[4]
  cursor.execute("INSERT OR IGNORE INTO categories (id, category_name, race_date) VALUES (?, ?, ?)", (None, original_category, race_date))


conn.commit()
cursor.execute("SELECT * from categories")
categories = cursor.fetchall()

mappings = {
  "Men Pro Senior": "Pro",
  "Men UCI Pro": "Pro",
  "Men  UCI": "Pro",
  "Men  Elite UCI": "Pro",
  "Saturday A 1/2/3": "Cat 1/2/3",
  "Cat 3/4 Category": "Cat 3/4",
  "Men Cat 5": "Cat 5",
  "Men Cat 4/Novice": "Cat 4/5",
  "Men Cat4/5 Elite": "Cat 4/5",
  "Men Cat 4/5 Elite": "Cat 4/5",
  "Men Category 4 Elite": "Cat 4",
  "Mens Cat 1/2/3": "Cat 1/2/3",
  "Saturday B 3/4": "Cat 3/4",
  "Category 3 Open": "Cat 3",
  "P/1/2/3 Pro/Cat 1/2/3": "Cat 1/2/3",
  "Men Cat 3/4 Elite": "Cat 3/4",
  "Cat 4/novice Category": "Cat 4/5",
  "Men Cat 4 Elite": "Cat 4",
  "Men SM Open": "Pro",
  "Men Senior Pro": "Pro",
  "Men Cat 2 Elite": "Cat 2",
  "Saturday C 4/5": "Cat 4/5",
  "Men OPEN  PRO/1/2/3": "Cat 1/2/3",
  "Men Senior Cat2": "Cat 2",
  "Men Elite 1/2/3": "Cat 1/2/3",
  "Men Open Pro 1/2/3": "Cat 1/2/3",
  "Senior Men Cat2": "Cat 2",
  "Men Senior Cat3": "Cat 3",
  "Men  3/4 and U19": "Cat 3/4",
  "C Race (Cat 4/5)": "Cat 4/5",
  "Sunday C 4/5": "Cat 4/5",
  "Sunday B 3/4": "Cat 3/4",
  "Senior Men Cat3": "Cat 3",
  "Men  Novice Wave 4a -": "Cat 5",
  "Men Novice: Wave 4a": "Cat 5",
  "Men Cat 4 Intermediate": "Cat 4",
  "Men M Novice": "Cat 5",
  "Men  Elite UCI": "Pro",
  "Men Cat 4/5 Elite": "Cat 4/5",
  "Men Cat 3 Elite": "Cat 3",
  "Men Cat 2 Elite": "Cat 2",
  "Men Cat4/5 Elite": "Cat 4/5",
  "Men Cat 4/Novice Elite": "Cat 4/5",
  "Men Cat 1/2/3 Elite": "Cat 1/2/3",
  "Cat 3/4 Category": "Cat 3/4",
  "Men Cat 4": "Cat 4",
  "Men Cat 3/4": "Cat 3/4",
  "Men Cat 1/2/3": "Cat 1/2/3",
  "P/1/2/3 Pro/Cat 1/2/3": "Pro",
  "Cat 4/novice Category": "Cat 4/5",
  "Men Cat 5": "Cat 5",
  "Men Senior Cat2": "Cat 2",
  "Men Senior Cat3": "Cat 3",
  "Men Cat 3/4 Elite": "Cat 3/4",
  "Men Cat 4 Elite": "Cat 4",
  "Men Cat 4/5": "Cat 4/5",
  "Men  1/2/3": "Cat 1/2/3",
  "Men  3/4 and U19": "Cat 3/4",
  "Senior Men Cat2": "Cat 2",
  "Senior Men Cat3": "Cat 3",
  "Men Cat 4/Novice": "Cat 4/5",
  "Men Category 1/2/3": "Cat 1/2/3",
  "Men Novice Elite": "Cat 5",
  "Men  UCI": "Pro",
  "Cat 5": "Cat 5",
  "Men Pro": "Pro",
  "Men Cat 2/3/4": "Cat 2/3/4",
  "Men Pro/1/2/3": "Cat 1/2/3",
  "Men Category 1/2/3 Elite": "Cat 1/2/3",
  "Men Category 4 Elite": "Cat 4",
  "Men Category 3/4 Elite": "Cat 3/4",
  "Men Pro/Cat 1/2/3": "Cat 1/2/3",
  "Men Pro/Cat 1/2": "Cat 1/2",
  "Men SM Open": "Pro",
  "Elite Men": "Pro",
  "Mens Cat 1/2/3": "Cat 1/2/3",
  "Men UCI Pro": "Pro",
  "Men Cat 1/2 Elite": "Cat 1/2",
  "Men Pro UCI": "Pro",
  "Men Pro Senior": "Pro",
  "C Race (Cat 4/5)": "Cat 4/5",
  "Saturday A 1/2/3": "Cat 1/2/3",
  "Saturday B 3/4": "Cat 3/4",
  "Saturday C 4/5": "Cat 4/5",
  "Sunday C 4/5": "Cat 4/5",
  "Sunday B 3/4": "Cat 3/4",
  "Men M Novice": "Cat 5",
  "Category 3 Open": "Cat 3",
  "Men Senior Pro": "Pro",
  "Men 1/2/3": "Cat 1/2/3",
  "Cat 1/2/3 Men": "Cat 1/2/3"
}

for category in categories:
  category_name = category[2]
  cursor.execute("UPDATE categories SET excluded=?, simple_category=?, excluded_reason=? WHERE category_name=?", (1, None, None, category_name))
  if eval(category[1][:4]) < 2023:
    cursor.execute("UPDATE categories SET excluded=?, excluded_reason=? WHERE category_name=?", (1, "Race too old", category_name)) 

  if any(x in category_name.upper() for x in excluded_not_elite):
    cursor.execute("UPDATE categories SET excluded=?, excluded_reason=? WHERE category_name=?", (1, "Not men's elite", category_name))

  if any(x in category_name.upper() for x in excluded_not_usac):
    cursor.execute("UPDATE categories SET excluded=?, excluded_reason=? WHERE category_name=?", (1, "Not USAC category/race", category_name))

conn.commit()
cursor.execute("SELECT * FROM categories WHERE excluded_reason IS NULL")
categories = cursor.fetchall()

for category in categories:
  category_name = category[2]
  simple_category = mappings[category_name]
  cursor.execute("UPDATE categories SET excluded=?, excluded_reason=?, simple_category=? WHERE category_name=?", (0, "N/A", simple_category, category_name))

conn.commit()
cursor.close()
conn.close()

