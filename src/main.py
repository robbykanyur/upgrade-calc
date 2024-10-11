import sys
import click
from migrations import run_migrations
from scrape_races import run_scraper
# from calculate_upgrade_points import calculate_upgrade_points

@click.command()
@click.option('-races', '--skip-races', is_flag=True, default=False)
@click.option('-riders', '--skip-riders', is_flag=True, default=False)

def run_app(skip_races, skip_riders):
  print("\nRunning database migrations")
  run_migrations()

  if not skip_races:
    print("\nScraping CCC races")
    run_scraper()
  else:
    print("\nSkipping race scraping")

  # print("Calculating upgrade points")
  # calculate_upgrade_points()

if __name__ == '__main__':
  run_app()