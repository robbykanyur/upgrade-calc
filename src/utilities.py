import os

def get_latest_scrape_dir(base_dir):
  directories = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
  if directories:
    latest_date = max(directories)
    return latest_date
  else:
    return None