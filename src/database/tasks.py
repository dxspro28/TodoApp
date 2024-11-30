import sqlite3

class Tasks:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                completed INTEGER
            )
        """)
        self.conn.commit()

    def add_task(self, title, description, completed=False):
        self.conn.execute("""
            INSERT INTO tasks (title, description, completed)
            VALUES (?, ?, ?)
        """, (title, description, completed))
        self.conn.commit()

    def get_tasks(self):
        return self.conn.execute("SELECT * FROM tasks").fetchall()

    def search_task(self, query):
        return self.conn.execute("""
            SELECT * FROM tasks
            WHERE title LIKE ? OR description LIKE ?
        """, (f"%{query}%", f"%{query}%")).fetchall()

    def update_task(self, id, title, description, completed):
        self.conn.execute("""
            UPDATE tasks SET title=?, description=?, completed=?
            WHERE id=?
        """, (title, description, completed, id))
        self.conn.commit()

    def delete_task(self, id):
        self.conn.execute("DELETE FROM tasks WHERE id=?", (id,))
        self.conn.commit()
