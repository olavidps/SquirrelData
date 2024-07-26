import os
import psycopg2
import psycopg2.extras

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")


class DatabaseManager:
    def __init__(self):
        self.connection = self.__connect()
        self.check_database_initialization()
        self.cursor = self.connection.cursor()
        self.dict_cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    @staticmethod
    def __connect():
        return psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host="postgres"
        )

    def check_database_initialization(self):
        cur = self.connection.cursor()

        # Create tables if they do not exist
        sql_stmt = """
        CREATE TABLE IF NOT EXISTS areas (
            id VARCHAR(10) PRIMARY KEY,
            name VARCHAR(255)
        );
        
        CREATE TABLE IF NOT EXISTS parks (
            id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255),
            other_animal_sightings VARCHAR(255),
            area_id VARCHAR(10) REFERENCES areas(id)
        );
        
        CREATE TABLE IF NOT EXISTS colors (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50)
        );
        
        CREATE TABLE IF NOT EXISTS squirrels (
            id VARCHAR(255) PRIMARY KEY,
            activities VARCHAR(255),
            park_id VARCHAR(50) REFERENCES parks(id),
            primary_fur_color_id INTEGER REFERENCES colors(id)
        );
        """
        cur.execute(sql_stmt)
        self.connection.commit()
        print("Database initialized successfully!")

    def store_data(self, table_name, primary_key, data, update_on_conflict=False):
        for row in data:
            columns = list(row.keys())
            column_names = ", ".join(columns)
            placeholders = ", ".join(["%s"] * len(columns))
            update_statements = ", ".join([f"{col} = EXCLUDED.{col}" for col in columns if col != primary_key])
            conflict_action = f"DO UPDATE SET {update_statements}" if update_on_conflict else "DO NOTHING"

            sql_stmt = f"""
                INSERT INTO {table_name} ({column_names})
                VALUES ({placeholders})
                ON CONFLICT ({primary_key}) {conflict_action}
            """

            self.cursor.execute(sql_stmt, tuple(row[col] for col in columns))
        self.connection.commit()

    def get_data(self, table_name, get_distinct=False):
        distinct_clause = "DISTINCT" if get_distinct else ""
        sql_stmt = f"SELECT {distinct_clause} * FROM {table_name}"
        self.dict_cursor.execute(sql_stmt)
        return self.dict_cursor.fetchall()
