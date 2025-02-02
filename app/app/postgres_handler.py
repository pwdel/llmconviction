import psycopg2
from psycopg2 import sql


class PostgresHandler:
    def __init__(self, host="postgres", port=5432, dbname="newsdb", user="youruser", password="yourpassword"):
        self.config = {
            "host": host,
            "port": port,
            "dbname": dbname,
            "user": user,
            "password": password,
        }
        self.conn = None
        self.connect()

    def connect(self):
        """Establish a connection to the Postgres database."""
        try:
            self.conn = psycopg2.connect(**self.config)
            self.conn.autocommit = True
            self.create_table()  # Ensure table exists when we connect
        except Exception as e:
            print(f"Error connecting to Postgres: {e}")
            raise

    def create_table(self):
        """Create the news table if it doesn't already exist."""
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS news (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    pub_date TEXT,
                    source TEXT
                )
            """)
            print("Ensured that the 'news' table exists.")

    def insert_news_items(self, news_items):
        """
        Insert multiple news items into the database.

        Parameters:
            news_items (list of tuple): Each tuple should have (title, pub_date, source)
        """
        with self.conn.cursor() as cur:
            insert_query = sql.SQL("""
                INSERT INTO news (title, pub_date, source)
                VALUES (%s, %s, %s)
            """)
            cur.executemany(insert_query, news_items)
            print(f"Inserted {len(news_items)} news items into the database.")

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("Closed the database connection.")
