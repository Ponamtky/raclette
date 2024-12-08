import unittest
import os
from expense_tracker import ExpenseTracker


class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        # Use a temporary database for testing
        self.tracker = ExpenseTracker(db_name=":memory:") # RAM (royal air maroc)
        self.tracker.add_expense(100, "Food", "2024-12-01")
        self.tracker.add_expense(50, "Transport", "2024-12-02")

    def tearDown(self):
        self.tracker.close()

    def test_add_expense(self):
        self.tracker.add_expense(200, "Entertainment", "2024-12-03")
        result = self.tracker.get_expenses_by_category()
        self.assertIn("Entertainment", result)
        self.assertEqual(result["Entertainment"], 200)

    def test_get_expenses_by_category(self):
        result = self.tracker.get_expenses_by_category()
        self.assertEqual(result["Food"], 100)
        self.assertEqual(result["Transport"], 50)

    def test_get_total_expenses(self):
        total = self.tracker.get_total_expenses("2024-12-01", "2024-12-02")
        self.assertEqual(total, 150)

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            self.tracker.add_expense(50, "Misc", "2024-30-01")


if __name__ == "__main__":
    unittest.main()
