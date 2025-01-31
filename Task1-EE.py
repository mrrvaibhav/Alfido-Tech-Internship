import pandas as pd
import matplotlib.pyplot as plt
import sqlite3


class FinanceTracker:
    def __init__(self, db_name="finance.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                category TEXT,
                amount REAL,
                type TEXT
            )
        ''')
        self.conn.commit()

    def add_transaction(self, date, category, amount, trans_type):
        self.cursor.execute('''
            INSERT INTO transactions (date, category, amount, type) 
            VALUES (?, ?, ?, ?)
        ''', (date, category, amount, trans_type))
        self.conn.commit()

    def get_transactions(self):
        return pd.read_sql("SELECT * FROM transactions", self.conn)

    def generate_report(self):
        df = self.get_transactions()
        if df.empty:
            print("No transactions recorded.")
            return
        print(df)

    def visualize_spending(self):
        df = self.get_transactions()
        if df.empty:
            print("No transactions to visualize.")
            return
        expenses = df[df['type'] == 'expense'].groupby('category')['amount'].sum()
        expenses.plot(kind='bar', title='Expenses by Category')
        plt.xlabel('Category')
        plt.ylabel('Amount')
        plt.show()

    def export_to_csv(self, filename="transactions.csv"):
        df = self.get_transactions()
        df.to_csv(filename, index=False)
        print(f"Data exported to {filename}")


# Usage Example
if __name__ == "__main__":
    tracker = FinanceTracker()
    tracker.add_transaction("2025-01-31", "Groceries", 50.0, "expense")
    tracker.add_transaction("2025-01-31", "Salary", 1500.0, "income")
    tracker.generate_report()
    tracker.visualize_spending()
    tracker.export_to_csv()
