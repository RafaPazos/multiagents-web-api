import sqlite3
from typing import Any

class InMemoryStorage:
    def __init__(self):
        self._storage = {}
        print("INFO:     InMemoryStorage initialized")

    def set(self, key, value):
        """Store a value with the given key."""
        self._storage[key] = value

    def get(self, key):
        """Retrieve a value by its key."""
        return self._storage.get(key)

    def get_all(self):
        """Retrieve all values from the storage."""
        return list(self._storage.values())

    def delete(self, key):
        """Delete a value by its key."""
        if key in self._storage:
            del self._storage[key]

    def clear(self):
        """Clear all stored values."""
        self._storage.clear()

    def keys(self):
        """Return all keys in the storage."""
        return list(self._storage.keys())

    def values(self):
        """Return all values in the storage."""
        return list(self._storage.values())

    def items(self):
        """Return all key-value pairs in the storage."""
        return list(self._storage.items())

    def __len__(self):
        """Return the number of items in the storage."""
        return len(self._storage)

    def __contains__(self, key):
        """Check if a key exists in the storage."""
        return key in self._storage
    

class SQLiteStorage:
    def __init__(self, db_path="data/app.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()
        print("INFO:     SQLiteStorage initialized")

    def _create_table(self):
        with self.conn:
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS storage (key TEXT PRIMARY KEY, value TEXT)"
            )
            self.conn.commit()
            print("INFO:     SQLiteStorage table created")

    def set(self, key: str, value: Any):
        with self.conn:
            self.conn.execute(
                "REPLACE INTO storage (key, value) VALUES (?, ?)", (key, str(value))
            )
            self.conn.commit()

    def get(self, key: str) -> Any:
        cur = self.conn.cursor()
        cur.execute("SELECT value FROM storage WHERE key = ?", (key,))
        row = cur.fetchone()
        return row[0] if row else None

    def get_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT value FROM storage")
        return [row[0] for row in cur.fetchall()]

    def delete(self, key: str):
        with self.conn:
            self.conn.execute("DELETE FROM storage WHERE key = ?", (key,))

    def clear(self):
        with self.conn:
            self.conn.execute("DELETE FROM storage")

    def keys(self):
        cur = self.conn.cursor()
        cur.execute("SELECT key FROM storage")
        return [row[0] for row in cur.fetchall()]

    def values(self):
        cur = self.conn.cursor()
        cur.execute("SELECT value FROM storage")
        return [row[0] for row in cur.fetchall()]

    def items(self):
        cur = self.conn.cursor()
        cur.execute("SELECT key, value FROM storage")
        return cur.fetchall()

    def __len__(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM storage")
        return cur.fetchone()[0]

    def __contains__(self, key):
        cur = self.conn.cursor()
        cur.execute("SELECT 1 FROM storage WHERE key = ?", (key,))
        return cur.fetchone() is not None