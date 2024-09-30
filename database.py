import sqlite3

class Database:
    def __init__(self, database_path):
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()

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