#!/usr/local/bin/python

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
            self.create_news_table()
            self.create_sentiment_table()
        except Exception as e:
            print(f"Error connecting to Postgres: {e}")
            raise

    def create_news_table(self):
        """Create the news table if it doesn't already exist."""
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS news (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    pub_date TIMESTAMPTZ,
                    source TEXT
                )
            """)
            print("Ensured that the 'news' table exists.")

    def create_sentiment_table(self):
        """Create the sentiment_results table if it doesn't already exist."""
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sentiment_results (
                    id SERIAL PRIMARY KEY,
                    sentiment JSON NOT NULL,
                    inserted_at TIMESTAMPTZ DEFAULT NOW(),
                    identifier TEXT
                )
            """)
            print("Ensured that the 'sentiment_results' table exists.")

    def fetch_all_news_headlines(self):
        """Fetch all news headlines from the database."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT title FROM news ORDER BY id;")
            records = cur.fetchall()
        return [record[0] for record in records]

    def fetch_news_headlines(self, topic=None, pub_date=None):
        """Fetch all news headlines from the database, optionally filtering by topic and publication date."""
        query = "SELECT title FROM news WHERE TRUE"
        params = []

        if topic:
            query += " AND LOWER(title) LIKE LOWER(%s)"
            params.append(f"%{topic}%")
        if pub_date:
            query += " AND DATE(pub_date) = %s"  # Assuming pub_date is of type 'date' or 'timestamp'
            params.append(pub_date)

        with self.conn.cursor() as cur:
            cur.execute(query, params)
            records = cur.fetchall()
        return [record[0] for record in records]

    def fetch_sentiment_results(self, identifier_filter):
        """
        Fetch sentiment results that match the given identifier filter.

        Parameters:
            identifier_filter (str): A string to filter the identifier column (using a case-insensitive match).

        Returns:
            list of tuple: Each tuple represents a row in the sentiment_results table.
        """
        with self.conn.cursor() as cur:
            query = """
                SELECT id, sentiment, inserted_at, identifier
                FROM sentiment_results
                WHERE identifier ILIKE %s
                ORDER BY inserted_at DESC;
            """
            cur.execute(query, (f"%{identifier_filter}%",))
            return cur.fetchall()

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

    def insert_sentiment_result(self, sentiment_json, identifier=None):
        """
        Insert a sentiment result into the sentiment_results table.

        Parameters:
            sentiment_json (dict or str): A JSON object (or string) representing the sentiment analysis result.
            identifier (str): Optional text identifier to label the result.
        """
        with self.conn.cursor() as cur:
            insert_query = sql.SQL("""
                INSERT INTO sentiment_results (sentiment, identifier)
                VALUES (%s, %s)
            """)
            cur.execute(insert_query, (sentiment_json, identifier))
            print("Inserted sentiment result into the database.")

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("Closed the database connection.")


# Simple test routine to verify the connection
if __name__ == "__main__":
    try:
        # Use default connection parameters or override with your own values
        handler = PostgresHandler(
            host="postgres",   # or "localhost" if testing locally
            port=5432,
            dbname="newsdb",
            user="youruser",
            password="yourpassword"
        )
        print("Connection to Postgres established and table ensured.")
    except Exception as e:
        print("Test failed:", e)
    finally:
        if 'handler' in locals():
            handler.close()
