# test_analytics.py

import unittest
import analytics

class TestAnalytics(unittest.TestCase):

    def test_total_revenue(self):
        revenue = analytics.get_total_revenue()
        print(f"Текущий доход: {revenue}")
        self.assertIsInstance(revenue, (int, float))
        self.assertGreaterEqual(revenue, 0)

    def test_total_sales_count(self):
        count = analytics.get_total_sales_count()
        print(f"Текущие продажи: {count}")
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)


if __name__ == '__main__':
    unittest.main()