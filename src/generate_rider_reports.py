import sqlite3
from datetime import datetime, timedelta
from time import strptime, mktime
from _constants import excluded_not_elite, excluded_not_usac, excluded_events

conn = sqlite3.connect('./db/main.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM upgrade_flags WHERE override IS NULL and warning IS NULL ORDER BY rider_id ASC")
flags = cursor.fetchall()
riders = {}
datestamp = datetime.now().strftime('%Y-%m-%d')

for flag in flags:
  riders[flag[1]] = []
for flag in flags:
  riders[flag[1]].append(flag)

  output = f"# Upgrade report for {datestamp}  \n  \n"

for rider in riders:
  entry = riders[rider]
  cursor.execute("SELECT * FROM riders WHERE id=?", (entry[0][1],))
  rider_details = cursor.fetchone()
  cursor.execute("SELECT * FROM results where rider_id=?", (entry[0][1],))
  rider_results = cursor.fetchall()

  output += f"## {rider_details[1]}  \n"
  output += f"- Category {rider_details[2]}  \n"
  output += f"- Age {rider_details[3]}  \n"
  output += f"- [www.crossresults.com/racer/{rider_details[0]}](https://www.crossresults.com/racer/{rider_details[0]})"
  output += f"\n\n"
  output += f"### Upgrade flags:  \n"
  for flag in entry:
    output += f"- {flag[3]} – {flag[4]}  \n"
  output += f"  \n### Results:  \n"
  for result in rider_results:
    try:
        numerical_result = eval(result[5])
    except:
      numerical_result = None

    try:
      rider_category = eval(rider_details[2])
    except:
      rider_category = 6

    valid_result = True
    if any(exclusion in result[4].upper() for exclusion in excluded_not_elite):
      valid_result = False
    if any(exclusion in result[4].upper() for exclusion in excluded_not_usac):
      valid_result = False
    if any(exclusion in result[3].upper() for exclusion in excluded_events):
      valid_result = False

    race_too_old = False
    race_date = datetime.fromtimestamp(mktime(strptime(result[2], "%Y-%m-%d")))
    if race_date < (datetime.now() - timedelta(days = 366)):
      race_too_old = True
      if rider_category < 5 and numerical_result != 1:
        valid_result = False

    if valid_result:
      output += f"- {result[3]} on {result[2]} (P{result[5][:-1]} of {result[6]} in {result[4]})  \n"
      if result[7] > 0 and str(rider_category) in result[4] and not race_too_old:
        output += f"  - {result[7]} UPGRADE POINTS  \n"

  output += "  \n---  \n  \n"

with open(f"./data/reports/{datestamp}.md", "w") as text_file:
  text_file.write(output)

conn.commit()
cursor.close()
conn.close()