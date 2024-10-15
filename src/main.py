import os
import click
import sqlite3
from migrations import run_migrations
from scrape_races import run_race_scraper
from create_rider_list import create_rider_list
from scrape_riders import run_rider_scraper
from parse_rider_file import process_rider_data
from calculate_upgrade_points import calculate_upgrade_points
from dotenv import load_dotenv
load_dotenv()

@click.command()
@click.option('-races', '--skip-races', is_flag=True, default=False)
@click.option('-riders', '--skip-riders', is_flag=True, default=False)

def run_app(skip_races, skip_riders):
  with sqlite3.connect(os.getenv('DB_PATH')) as conn:
    print("\nRunning database migrations")
    run_migrations(conn)

    if not skip_races:
      print("\nScraping CCC races")
      run_race_scraper(conn)
    else:
      print("\nSkipping race scraping")

    print("\nBuilding rider list")
    create_rider_list(conn)

    if not skip_riders:
      print("\nScraping CCC riders")
      run_rider_scraper(conn)
    else:
      print("\nSkipping rider scraping")

    print("\nParsing results")
    process_rider_data(conn)

    print("\nCalculating upgrade points")
    calculate_upgrade_points(conn)

if __name__ == '__main__':
  run_app()