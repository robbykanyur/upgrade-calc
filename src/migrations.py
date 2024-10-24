from _constants import ccc_races

def enable_foreign_keys(conn):
  conn.execute("PRAGMA foreign_keys = 1")
  conn.commit()

def create_tables(conn):
  tables = {
    "races": """
      CREATE TABLE IF NOT EXISTS races (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        crossresults_id TEXT NOT NULL UNIQUE
      )
    """,
    "riders": """
      CREATE TABLE IF NOT EXISTS riders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        current_category TEXT,
        age INTEGER
      )
    """,
    "results": """
      CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rider_id INTEGER NOT NULL,
        race_date TEXT NOT NULL,
        race_name TEXT NOT NULL,
        race_category TEXT NOT NULL,
        race_position TEXT NOT NULL,
        race_starters INTEGER NOT NULL,
        age_at_race INTEGER NOT NULL,
        upgrade_points INTEGER,
        FOREIGN KEY (rider_id) REFERENCES riders (id) ON DELETE CASCADE
      )
    """,
    "categories": """
      CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        race_date TEXT NOT NULL,
        category_name TEXT UNIQUE NOT NULL,
        simple_category TEXT,
        excluded INTEGER DEFAULT 0,
        mixed_field INTEGER DEFAULT 0
      )
    """,
    "upgrade_points": """
      CREATE TABLE IF NOT EXISTS upgrade_points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rider_id INTEGER NOT NULL UNIQUE,
        date_calculated TEXT NOT NULL,
        upgrade_points REAL NOT NULL,
        cat_5_races INTEGER DEFAULT 0,
        qualified_wins INTEGER DEFAULT 0,
        FOREIGN KEY (rider_id) REFERENCES riders (id) ON DELETE CASCADE
      )
    """,
    "upgrade_flags": """
      CREATE TABLE IF NOT EXISTS upgrade_flags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rider_id INTEGER NOT NULL,
        date_calculated TEXT NOT NULL,
        reason TEXT NOT NULL,
        details TEXT NOT NULL,
        warning TEXT,
        override TEXT,
        FOREIGN KEY (rider_id) REFERENCES riders (id) ON DELETE CASCADE
      )
    """
  }

  cursor = conn.cursor()
  for table_name, create_table_sql in tables.items():
    cursor.execute(create_table_sql)
  conn.commit()

def seed_races(conn, ccc_races):
  cursor = conn.cursor()
  cursor.executemany('''
    INSERT OR IGNORE INTO races (name, date, crossresults_id)
    VALUES (?, ?, ?)               
  ''', ccc_races)
  conn.commit()

def run_migrations(conn):
  enable_foreign_keys(conn)
  create_tables(conn)
  seed_races(conn, ccc_races)