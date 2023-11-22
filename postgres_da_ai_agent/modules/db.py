import psycopg2
from contextlib import contextmanager
from psycopg2 import sql

class PostgresManager:
    def __init__(self, db_url):
        self.db_url = db_url

    def __enter__(self):
        self.conn = self.connect_with_url()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def connect_with_url(self):
        self.conn = psycopg2.connect(self.db_url)
        return self.conn

    def upsert(self, table_name, _dict):
        with self.conn.cursor() as cursor:
            columns = _dict.keys()
            values = _dict.values()
            on_conflict_set = sql.SQL(', ').join(
                sql.SQL("{} = EXCLUDED.{}").format(sql.Identifier(k), sql.Identifier(k))
                for k in columns if k != 'Id'
            )
            query = sql.SQL("""
                INSERT INTO {} ({}) VALUES ({}) ON CONFLICT (Id) DO UPDATE SET {}
            """).format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(values)),
                on_conflict_set
            )
            cursor.execute(query, list(values))
            self.conn.commit()

    def delete(self, table_name, _id):
        with self.conn.cursor() as cursor:
            query = sql.SQL("DELETE FROM {} WHERE Id = %s").format(sql.Identifier(table_name))
            cursor.execute(query, (_id,))
            self.conn.commit()

    def get(self, table_name, _id):
        with self.conn.cursor() as cursor:
            query = sql.SQL("SELECT * FROM {} WHERE Id = %s").format(sql.Identifier(table_name))
            cursor.execute(query, (_id,))
            return cursor.fetchone()

    def get_all(self, table_name):
        with self.conn.cursor() as cursor:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
            cursor.execute(query)
            return cursor.fetchall()

    def run_sql(self, sql_statement):
        with self.conn.cursor() as cursor:
            cursor.execute(sql_statement)
            self.conn.commit()
            try:
                return cursor.fetchall()
            except psycopg2.ProgrammingError:
                return None  # In case the SQL does not return a result

    def get_table_definition(self, table_name):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = %s
            """, (table_name,))
            columns = cursor.fetchall()
            create_table_statement = f"CREATE TABLE {table_name} ("
            create_table_statement += ", ".join([f"{col[0]} {col[1]}{' NOT NULL' if col[2] == 'NO' else ''}{' DEFAULT ' + col[3] if col[3] else ''}" for col in columns])
            create_table_statement += ");"
            return create_table_statement

    def get_all_table_names(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public'
            """)
            return [table[0] for table in cursor.fetchall()]

    def get_table_definition_for_prompt(self):
        table_names = self.get_all_table_names()
        definitions = [self.get_table_definition(table_name) for table_name in table_names]
        return '\n'.join(definitions)