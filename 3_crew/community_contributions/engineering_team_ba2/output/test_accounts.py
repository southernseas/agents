import unittest
from datetime import datetime
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        Account._all_users = {}
    
    def test_register_account(self):
        Account.register("user@example.com", "password123")
        self.assertEqual(len(Account._all_users), 1)
        user = Account._all_users["user@example.com"]
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.funds, 0)
    
    def test_register_duplicate_email(self):
        with self.assertRaises(ValueError):
            Account.register("user@example.com", "password123")
            Account.register("user@example.com", "password321")
    
    def test_login_valid(self):
        Account.register("user@example.com", "password123")
        user = Account.login("user@example.com", "password123")
        self.assertEqual(user.email, "user@example.com")
    
    def test_login_invalid_credentials(self):
        with self.assertRaises(ValueError):
            Account.login("nonexistent@example.com", "password")
        Account.register("user@example.com", "password123")
        with self.assertRaises(ValueError):
            Account.login("user@example.com", "wrongpassword")
    
    def test_deposit_funds(self):
        user = Account.register("user@example.com", "password")
        user.deposit_funds(1000)
        self.assertEqual(user.funds, 1000)
        self.assertEqual(user.initial_deposit, 1000)
        user.deposit_funds(500)
        self.assertEqual(user.funds, 1500)
        self.assertEqual(user.initial_deposit, 1000)
    
    def test_withdraw_funds(self):
        user = Account.register("user@example.com", "password")
        user.deposit_funds(1000)
        user.withdraw_funds(500)
        self.assertEqual(user.funds, 500)
        with self.assertRaises(ValueError):
            user.withdraw_funds(600)
    
    def test_buy_shares(self):
        user = Account.register("user@example.com", "password")
        user.deposit_funds(1000)
        user.buy_shares("AAPL", 2)
        self.assertEqual(user.holdings["AAPL"], 2)
        self.assertEqual(user.funds, 700)
        self.assertIn("AAPL", user.holdings)
    
    def test_buy_shares_insufficient_funds(self):
        user = Account.register("user@example.com", "password")
        with self.assertRaises(ValueError):
            user.buy_shares("AAPL", 10)
    
    def test_sell_shares(self):
        user = Account.register("user@example.com", "password")
        user.deposit_funds(1000)
        user.buy_shares("AAPL", 5)
        user.sell_shares("AAPL", 2)
        self.assertEqual(user.holdings["AAPL"], 3)
        self.assertEqual(user.funds, 1000 + 300)
    
    def test_sell_shares_invalid_quantity(self):
        user = Account.register("user@example.com", "password")
        with self.assertRaises(ValueError):
            user.sell_shares("AAPL", 1)
        user.deposit_funds(1000)
        user.buy_shares("AAPL", 2)
        with self.assertRaises(ValueError):
            user.sell_shares("AAPL", 3)
    
    def test_transaction_history(self):
        user = Account.register("user@example.com", "password")
        user.deposit_funds(1000)
        self.assertEqual(len(user.transaction_history), 1)

if __name__ == "__main__":
    unittest.main()