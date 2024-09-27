import sqlite3

class Database:
    def __init__(self, database_path):
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()

    def extract_schema(self):
        schema_info = []
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        for table in tables:
            table_name = table[0]  # Extract the table name from the tuple
            self.cursor.execute(f"PRAGMA table_info('{table_name}');")
            columns = self.cursor.fetchall()
            self.cursor.execute(f"PRAGMA foreign_key_list('{table_name}');")
            foreign_keys = self.cursor.fetchall()
            schema_info.append({
                'table_name': table_name,
                'columns': columns,
                'foreign_keys': foreign_keys
            })
        return schema_info

    def execute_query(self, query):
        try:
            self.cursor.execute(query.strip())
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print("SQLite Error:", e)
            if hasattr(e, 'sqlite_errorcode'):
                print("SQLite Error Code:", e.sqlite_errorcode)
            if hasattr(e, 'sqlite_errorname'):
                print("SQLite Error Name:", e.sqlite_errorname)
            return None

    def close_connection(self):
        self.cursor.close()
        self.conn.close()