import os
from pathlib import Path
from scrape_riders import scrape_rider

def scrape_single_rider(rider_id, datestamp):
  if (not rider_id) or (not datestamp):
    print("Please provide both rider id and datestamp (YYYY-MM-DD) with -id and -date flags")
  else:
    save_path = Path(f'./data/riders/{datestamp}')
    rider_id = str(rider_id)

    if not os.path.exists(save_path):
      os.makedirs(save_path)
    scrape_rider(rider_id, save_path)