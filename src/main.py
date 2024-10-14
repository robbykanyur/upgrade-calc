import click
from migrations import run_migrations
from scrape_races import run_race_scraper
from create_rider_list import create_rider_list
from scrape_riders import run_rider_scraper
# from calculate_upgrade_points import calculate_upgrade_points

@click.command()
@click.option('-races', '--skip-races', is_flag=True, default=False)
@click.option('-riders', '--skip-riders', is_flag=True, default=False)

def run_app(skip_races, skip_riders):
  print("\nRunning database migrations")
  run_migrations()

  if not skip_races:
    print("\nScraping CCC races")
    run_race_scraper()
  else:
    print("\nSkipping race scraping")

  print("\nBuilding rider list")
  create_rider_list()

  print("\nScraping CCC riders")
  run_rider_scraper()

  # print("Calculating upgrade points")
  # calculate_upgrade_points()

if __name__ == '__main__':
  run_app()