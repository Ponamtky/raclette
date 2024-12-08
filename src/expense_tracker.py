import sqlite3
from datetime import datetime


class ExpenseTracker:
    def __init__(self, db_name="expenses.db"):
        self.conn = sqlite3.connect(db_name)
        self._create_table()

    def _create_table(self):
        """Creates the expenses table if it doesn't already exist."""
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL
                )
                """
            )

    def add_expense(self, amount, category, date):
        """Adds a new expense to the database."""
        try:
            datetime.strptime(date, "%Y-%m-%d")  # Validate date format
            with self.conn:
                self.conn.execute(
                    "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
                    (amount, category, date),
                )
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    def get_expenses_by_category(self):
        """Returns expenses grouped by category."""
        query = "SELECT category, SUM(amount) FROM expenses GROUP BY category"
        with self.conn:
            rows = self.conn.execute(query).fetchall()
        return {row[0]: row[1] for row in rows}

    def get_total_expenses(self, start_date, end_date):
        """Calculates total expenses for a given date range."""
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
            query = """
                SELECT SUM(amount) FROM expenses
                WHERE date BETWEEN ? AND ?
            """
            with self.conn:
                total = self.conn.execute(query, (start_date, end_date)).fetchone()[0]
            return total if total else 0
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    def close(self):
        """Closes the database connection."""
        self.conn.close()
