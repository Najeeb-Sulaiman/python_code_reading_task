import json
import logging
from datetime import datetime
from typing import List, Dict

logging.basicConfig(level=logging.INFO)


class Transaction:
    """
    Represents a financial transaction.
    """

    def __init__(self, date: str, amount: float, category: str):
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.amount = amount
        self.category = category

    def __repr__(self):
        return f"<Transaction {self.amount} {self.category} on {self.date.date()}>"  # noqa: E501

    def is_expense(self):
        return self.amount < 0


class BudgetAnalyzer:
    """
    Analyzes a list of transactions to produce financial insights.
    """

    def __init__(self, transactions: List[Transaction]):
        self.transactions = transactions

    def total_spent(self) -> float:
        return sum(t.amount for t in self.transactions if t.is_expense())

    def total_earned(self) -> float:
        return sum(t.amount for t in self.transactions if not t.is_expense())

    def spending_by_category(self) -> Dict[str, float]:
        summary = {}
        for t in self.transactions:
            if t.is_expense():
                summary[t.category] = summary.get(t.category, 0) + abs(t.amount)  # noqa: E501
        return summary

    def print_summary(self):
        logging.info("------ Budget Summary ------")
        logging.info(f"Total Earned: ${self.total_earned():.2f}")
        logging.info(f"Total Spent:  ${abs(self.total_spent()):.2f}")
        logging.info("Spending by Category:")
        for category, amount in self.spending_by_category().items():
            logging.info(f"  {category}: ${amount:.2f}")


def load_transactions(filepath: str) -> List[Transaction]:
    """
    Load transactions from a JSON file.
    JSON format:
    [
        {"date": "2024-05-01", "amount": -50.25, "category": "groceries"},
        {"date": "2024-05-02", "amount": 2000.00, "category": "salary"}
    ]
    """
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return [Transaction(**item) for item in data]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load transactions: {e}")
        return []


def main():
    filepath = "BudgetAnalyzer/transactions.json"
    transactions = load_transactions(filepath)

    if not transactions:
        logging.warning("No transactions to analyze.")
        return

    analyzer = BudgetAnalyzer(transactions)
    analyzer.print_summary()


if __name__ == "__main__":
    main()
