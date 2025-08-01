import unittest
import datetime
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        # Create a valid account for testing
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'Password1'
        self.account = Account(self.username, self.email, self.password)

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            Account('user1', 'notanemail', 'Password1')

    def test_invalid_password(self):
        # Too short
        with self.assertRaises(ValueError):
            Account('user2', 'user2@example.com', 'Pass1')
        # Missing digit
        with self.assertRaises(ValueError):
            Account('user2', 'user2@example.com', 'Password')
        # Missing uppercase
        with self.assertRaises(ValueError):
            Account('user2', 'user2@example.com', 'password1')
        # Missing lowercase
        with self.assertRaises(ValueError):
            Account('user2', 'user2@example.com', 'PASSWORD1')

    def test_successful_login(self):
        # Test correct login
        result = self.account.login(self.password)
        self.assertTrue(result)
        self.assertIsNotNone(self.account.session)
        self.assertTrue(self.account.session.get('logged_in', False))

    def test_unsuccessful_login(self):
        # Test wrong password
        result = self.account.login('WrongPass')
        self.assertFalse(result)
        self.assertIsNone(self.account.session)

    def test_deposit_funds(self):
        # Deposit valid funds
        initial_balance = self.account.balance
        deposit_amount = 1000.0
        self.account.deposit_funds(deposit_amount)
        self.assertEqual(self.account.balance, initial_balance + deposit_amount)

        # Check that initial_deposit is recorded
        self.assertEqual(self.account.initial_deposit, deposit_amount)

        # Test deposit transaction recorded
        transactions = self.account.get_transactions()
        self.assertTrue(any(t['type'] == 'deposit' and t['amount'] == deposit_amount for t in transactions))

        # Deposit invalid (non-positive) amount
        with self.assertRaises(ValueError):
            self.account.deposit_funds(0)
        with self.assertRaises(ValueError):
            self.account.deposit_funds(-100)

    def test_withdraw_funds_success(self):
        # Deposit funds then withdraw a valid amount
        deposit_amount = 500.0
        self.account.deposit_funds(deposit_amount)
        result = self.account.withdraw_funds(200.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, deposit_amount - 200.0)

        # Check transaction recorded
        transactions = self.account.get_transactions()
        self.assertTrue(any(t['type'] == 'withdrawal' and t['amount'] == 200.0 for t in transactions))

    def test_withdraw_funds_insufficient(self):
        # Deposit funds then try to withdraw more than balance
        self.account.deposit_funds(300.0)
        result = self.account.withdraw_funds(400.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 300.0)

    def test_buy_shares_success(self):
        # Deposit enough funds to buy 2 shares of AAPL at $150
        self.account.deposit_funds(500.0)
        result = self.account.buy_shares('AAPL', 2)
        self.assertTrue(result)
        # Balance should deduct the total cost
        expected_balance = 500.0 - (2 * get_share_price('AAPL'))
        self.assertAlmostEqual(self.account.balance, expected_balance)
        # Holdings updated
        self.assertEqual(self.account.holdings.get('AAPL'), 2)

    def test_buy_shares_invalid_quantity(self):
        self.account.deposit_funds(500.0)
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', 0)
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', -5)

    def test_buy_shares_insufficient_funds(self):
        # Deposit lower funds than needed
        self.account.deposit_funds(100.0)
        result = self.account.buy_shares('AAPL', 1)  # need 150
        self.assertFalse(result)
        self.assertNotIn('AAPL', self.account.holdings)

    def test_sell_shares_success(self):
        # Deposit funds, buy shares, then sell one share
        self.account.deposit_funds(1000.0)
        buy_result = self.account.buy_shares('TSLA', 2)  # 2 TSLA shares @250 each
        self.assertTrue(buy_result)
        sell_result = self.account.sell_shares('TSLA', 1)
        self.assertTrue(sell_result)
        # Holdings should be updated
        self.assertEqual(self.account.holdings.get('TSLA'), 1)
        # Balance should increase by TSLA share price
        expected_balance = 1000.0 - (2 * get_share_price('TSLA')) + get_share_price('TSLA')
        self.assertAlmostEqual(self.account.balance, expected_balance)

    def test_sell_shares_insufficient_shares(self):
        # Deposit funds, buy shares then try to sell more than owned
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('GOOGL', 1)  # 1 share of GOOGL
        result = self.account.sell_shares('GOOGL', 2)
        self.assertFalse(result)
        # Holdings remain unchanged
        self.assertEqual(self.account.holdings.get('GOOGL'), 1)

    def test_sell_shares_invalid_quantity(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 1)
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', 0)
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', -3)

    def test_calculate_portfolio_value(self):
        # Deposit and buy shares then calculate portfolio value
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 2)  # 2 * 150 = 300
        self.account.buy_shares('TSLA', 1)  # 1 * 250 = 250
        portfolio_value = self.account.calculate_portfolio_value()
        expected_value = 2 * get_share_price('AAPL') + 1 * get_share_price('TSLA')
        self.assertAlmostEqual(portfolio_value, expected_value)

    def test_compute_profit_or_loss(self):
        # Deposit funds, then simulate trading to impact profit/loss
        deposit = 1000.0
        self.account.deposit_funds(deposit)
        # No trades, profit/loss should be balance - initial_deposit (0 profit here)
        profit = self.account.compute_profit_or_loss()
        self.assertAlmostEqual(profit, self.account.balance - deposit)
        
        # Buy shares and then sell them to generate profit
        self.account.buy_shares('AAPL', 2)  # Spend 300, balance becomes 700
        self.account.sell_shares('AAPL', 2)  # Get back 300, balance becomes 1000 again
        profit = self.account.compute_profit_or_loss()
        self.assertAlmostEqual(profit, self.account.balance + self.account.calculate_portfolio_value() - deposit)

    def test_get_holdings_report(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 3)
        report = self.account.get_holdings_report()
        self.assertIn('AAPL', report)
        self.assertEqual(report['AAPL']['quantity'], 3)
        self.assertAlmostEqual(report['AAPL']['current_price'], get_share_price('AAPL'))
        self.assertAlmostEqual(report['AAPL']['total_value'], 3 * get_share_price('AAPL'))

    def test_get_transactions(self):
        # Initially no transactions
        self.assertEqual(self.account.get_transactions(), [])
        self.account.deposit_funds(500.0)
        self.account.withdraw_funds(100.0)
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 2)
        types = [t['type'] for t in transactions]
        self.assertIn('deposit', types)
        self.assertIn('withdrawal', types)

    def test_get_portfolio_summary(self):
        self.account.deposit_funds(1500.0)
        self.account.buy_shares('TSLA', 2)  # 2*250 = 500
        summary = self.account.get_portfolio_summary()
        expected_portfolio_value = self.account.calculate_portfolio_value()
        expected_balance = self.account.balance
        expected_profit_loss = expected_balance + expected_portfolio_value - self.account.initial_deposit
        self.assertAlmostEqual(summary['portfolio_value'], expected_portfolio_value)
        self.assertAlmostEqual(summary['available_balance'], expected_balance)
        self.assertAlmostEqual(summary['total_profit_loss'], expected_profit_loss)

    def test_static_get_bond_interest_rates(self):
        rates = Account.get_bond_interest_rates()
        self.assertTrue(isinstance(rates, dict))
        # Check some known rates
        self.assertAlmostEqual(rates.get('1-month'), 0.5)
        self.assertAlmostEqual(rates.get('10-year'), 3.5)

    def test_static_get_current_share_prices(self):
        symbols = ['AAPL', 'TSLA', 'GOOGL', 'INVALID']
        prices = Account.get_current_share_prices(symbols)
        self.assertTrue(isinstance(prices, dict))
        self.assertAlmostEqual(prices.get('AAPL'), get_share_price('AAPL'))
        self.assertAlmostEqual(prices.get('TSLA'), get_share_price('TSLA'))
        self.assertAlmostEqual(prices.get('GOOGL'), get_share_price('GOOGL'))
        # For an invalid symbol, price should be 0.0
        self.assertAlmostEqual(prices.get('INVALID'), 0.0)

if __name__ == '__main__':
    unittest.main()