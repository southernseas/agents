import unittest
import accounts
from datetime import datetime

class TestAccounts(unittest.TestCase):
    def setUp(self):
        """Reset the accounts registry before each test"""
        accounts.Account._accounts = {}

    def test_register_new_account_successfully(self):
        """Test account registration with valid credentials"""
        result = accounts.Account.register("testuser", "test@example.com", "password123")
        self.assertTrue(result)
        self.assertIn("testuser", accounts.Account._accounts)

    def test_register_existing_username_fails(self):
        """Test account registration with existing username"""
        accounts.Account.register("testuser", "test@example.com", "password")
        with self.assertRaises(ValueError):
            accounts.Account.register("testuser", "another@example.com", "password")

    def test_register_existing_email_fails(self):
        """Test account registration with existing email"""
        accounts.Account.register("testuser", "test@example.com", "password")
        with self.assertRaises(ValueError):
            accounts.Account.register("anotheruser", "test@example.com", "password")

    def test_login_with_username_and_password(self):
        """Test successful login with username and password"""
        accounts.Account.register("user", "user@example.com", "pass")
        account = accounts.Account.login("user", "pass")
        self.assertIsNotNone(account)
        self.assertEqual(account.username, "user")

    def test_login_with_email_and_password(self):
        """Test successful login with email and password"""
        accounts.Account.register("user", "email@example.com", "pass")
        account = accounts.Account.login("email@example.com", "pass")
        self.assertIsNotNone(account)

    def test_login_invalid_password_returns_none(self):
        """Test login with invalid password returns None"""
        accounts.Account.register("user", "user@example.com", "correctpass")
        account = accounts.Account.login("user", "wrongpass")
        self.assertIsNone(account)

    def test_deposit_funds_increases_balance(self):
        """Test depositing funds increases account balance"""
        account = accounts.Account.register("user", "email@example.com", "password")
        accounts.Account._accounts["user"].deposit_funds(100.0)
        self.assertEqual(accounts.Account._accounts["user"].balance, 100.0)

    def test_deposit_negative_amount_raises_error(self):
        """Test depositing negative amount raises ValueError"""
        account = accounts.Account.register("user", "email@example.com", "password")
        with self.assertRaises(ValueError):
            accounts.Account._accounts["user"].deposit_funds(-50.0)

    def test_withdraw_sufficient_funds(self):
        """Test withdrawal with sufficient funds"""
        account = accounts.Account.register("user", "email@example.com", "password")
        accounts.Account._accounts["user"].deposit_funds(200)
        accounts.Account._accounts["user"].withdraw_funds(100)
        self.assertEqual(accounts.Account._accounts["user"].balance, 100)

    def test_withdraw_insufficient_funds_raises(self):
        """Test withdrawal with insufficient funds raises ValueError"""
        account = accounts.Account.register("user", "email@example.com", "password")
        accounts.Account._accounts["user"].deposit_funds(50)
        with self.assertRaises(ValueError):
            accounts.Account._accounts["user"].withdraw_funds(100)

    def test_buy_stock_with_sufficient_funds(self):
        """Test buying stock with sufficient funds"""
        account = accounts.Account.register("user", "email@example.com", "password")
        accounts.Account._accounts["user"].deposit_funds(1000)
        accounts.Account._accounts["user"].buy_stock("AAPL", 5)
        self.assertEqual(accounts.Account._accounts["user"].holdings["AAPL"], 5)
        self.assertAlmostEqual(accounts.Account._accounts["user"].balance, 900.0)

    def test_buy_stock_insufficient_funds_raises(self):
        """Test buying stock with insufficient funds raises ValueError"""
        account = accounts.Account.register("user", "email@example.com", "password")
        with self.assertRaises(ValueError):
            accounts.Account._accounts["user"].buy_stock("AAPL", 5)

    def test_sell_stock_with_sufficient_shares(self):
        """Test selling stock with sufficient shares"""
        account = accounts.Account.register("user", "email@example.com", "password")
        accounts.Account._accounts["user"].deposit_funds(1000)
        accounts.Account._accounts["user"].buy_stock("AAPL", 5)
        accounts.Account._accounts["user"].sell_stock("AAPL", 2)
        self.assertEqual(accounts.Account._accounts["user"].holdings["AAPL"], 3)
        self.assertAlmostEqual(accounts.Account._accounts["user"].balance, 1090.0)

    def test_sell_stock_insufficient_shares_raises(self):
        """Test selling stock with insufficient shares raises ValueError"""
        account = accounts.Account.register("user", "email@example.com", "password")
        accounts.Account._accounts["user"].deposit_funds(1000)
        accounts.Account._accounts["user"].buy_stock("AAPL", 2)
        with self.assertRaises(ValueError):
            accounts.Account._accounts["user"].sell_stock("AAPL", 3)

    def test_sell_all_shares_removes_from_holdings(self):
        """Test selling all shares removes from holdings"""
        account = accounts.Account.register("user", "email@example.com", "password")
        accounts.Account._accounts["user"].deposit_funds(1000)
        accounts.Account._accounts["user"].buy_stock("AAPL", 3)
        accounts.Account._accounts["user"].sell_stock("AAPL", 3)
        self.assertNotIn("AAPL", accounts.Account._accounts["user"].holdings)

    def test_calculate_portfolio_value(self):
        """Test portfolio value calculation"""
        account = accounts.Account.register("user", "email@example.com", "password")
        accounts.Account._accounts["user"].deposit_funds(1000)
        accounts.Account._accounts["user"].buy_stock("AAPL", 2)
        accounts.Account._accounts["user"].buy_stock("TSLA", 1)
        portfolio_value = accounts.Account._accounts["user"].calculate_portfolio_value()
        expected_value = 920.0 + 2 * 150.0 + 1 * 180.0
        self.assertAlmostEqual(portfolio_value, expected_value)

    def test_calculate_profit_loss(self):
        """Test profit/loss calculation"""
        account = accounts.Account.register("user", "email@example.com", "password")
        accounts.Account._accounts["user"].deposit_funds(1000)
        accounts.Account._accounts["user"].buy_stock("AAPL", 2)
        accounts.Account._accounts["user"].buy_stock("TSLA", 1)
        profit_loss = accounts.Account._accounts["user"].calculate_profit_loss()
        self.assertAlmostEqual(profit_loss, 0.0)

    def test_get_current_share_prices(self):
        """Test get_current_share_prices returns correct values"""
        prices = accounts.get_current_share_prices()
        self.assertAlmostEqual(prices["AAPL"], 150.0)
        self.assertAlmostEqual(prices["TSLA"], 180.0)
        self.assertAlmostEqual(prices["GOOGL"], 2800.0)

    def test_get_bond_interest_rates(self):
        """Test get_bond_interest_rates returns correct structure"""
        rates = accounts.get_bond_interest_rates()
        self.assertAlmostEqual(rates["1-month"], 0.05)
        self.assertIn("30-year", rates)

    def test_get_currency_rates(self):
        """Test get_currency_rates returns correct base currency"""
        rates = accounts.get_currency_rates()
        self.assertEqual(rates["USD"], 1.0)
        self.assertAlmostEqual(rates["EUR"], 0.85)

    def test_get_latest_news(self):
        """Test get_latest_news returns headlines"""
        news = accounts.get_latest_news()
        self.assertEqual(len(news), 5)
        self.assertIn("Tech stocks rally", news[0])

    def test_transaction_repr_for_buy(self):
        """Test transaction representation for buy action"""
        transaction = accounts.Transaction("AAPL", 5, "buy", datetime(2023, 1, 1, 12, 34, 56))
        self.assertEqual(repr(transaction), "Bought 5 shares of AAPL at 2023-01-01 12:34:56")

    def test_transaction_repr_for_sell(self):
        """Test transaction representation for sell action"""
        transaction = accounts.Transaction("TSLA", 3, "sell", datetime(2023, 1, 1, 12, 34, 56))
        self.assertEqual(repr(transaction), "Sold 3 shares of TSLA at 2023-01-01 12:34:56")

if __name__ == "__main__":
    unittest.main()