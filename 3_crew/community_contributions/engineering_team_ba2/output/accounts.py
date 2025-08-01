import datetime
import re
from typing import Dict, List, Optional, Tuple

# Mock market data function as specified
def get_share_price(symbol: str) -> float:
    """
    Returns current share price for given symbol.
    Fixed prices for testing: AAPL ($150), TSLA ($250), GOOGL ($2700)
    """
    prices = {
        'AAPL': 150.0,
        'TSLA': 250.0,
        'GOOGL': 2700.0
    }
    return prices.get(symbol.upper(), 0.0)

class Account:
    """
    Account class for trading simulation platform.
    Manages user accounts, transactions, holdings, and portfolio calculations.
    """
    
    def __init__(self, username: str, email: str, password: str):
        """
        Initialize new account with given credentials.
        
        Args:
            username: Unique username
            email: Valid email address
            password: Secure password (will be validated)
        """
        # Validate email format
        if not self._validate_email(email):
            raise ValueError("Invalid email format")
            
        # Validate password complexity
        if not self._validate_password(password):
            raise ValueError("Password must be at least 8 characters with uppercase, lowercase, and number")
        
        self.username = username
        self.email = email
        self.password = password  # In production, store hash instead
        self.balance = 0.0
        self.initial_deposit = 0.0
        self.holdings = {}  # symbol -> quantity
        self.transactions = []
        self.session = None  # Simple session tracking
        
    def _validate_email(self, email: str) -> bool:
        """Validate email format using regex."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
        
    def _validate_password(self, password: str) -> bool:
        """Validate password complexity."""
        if len(password) < 8:
            return False
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        return has_upper and has_lower and has_digit
    
    def login(self, password: str) -> bool:
        """
        Authenticate user login.
        
        Args:
            password: Password to verify
            
        Returns:
            bool: True if login successful, False otherwise
        """
        if password == self.password:
            self.session = {'logged_in': True, 'timestamp': datetime.datetime.now()}
            return True
        return False
    
    def deposit_funds(self, amount: float) -> None:
        """
        Deposit funds into account.
        
        Args:
            amount: Amount to deposit (must be positive)
            
        Raises:
            ValueError: If amount is not positive
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
            
        self.balance += amount
        
        # Set initial deposit if first deposit
        if self.initial_deposit == 0:
            self.initial_deposit = amount
            
        # Record transaction
        self._record_transaction(
            transaction_type='deposit',
            amount=amount,
            symbol=None,
            quantity=None
        )
    
    def withdraw_funds(self, amount: float) -> bool:
        """
        Withdraw funds from account.
        
        Args:
            amount: Amount to withdraw (must be positive)
            
        Returns:
            bool: True if withdrawal successful, False if insufficient funds
            
        Raises:
            ValueError: If amount is not positive
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
            
        if amount > self.balance:
            return False
            
        self.balance -= amount
        
        # Record transaction
        self._record_transaction(
            transaction_type='withdrawal',
            amount=amount,
            symbol=None,
            quantity=None
        )
        
        return True
    
    def buy_shares(self, symbol: str, quantity: int) -> bool:
        """
        Buy shares of a stock.
        
        Args:
            symbol: Stock symbol to buy
            quantity: Number of shares to buy
            
        Returns:
            bool: True if purchase successful, False if insufficient funds
            
        Raises:
            ValueError: If quantity is not positive
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
            
        symbol = symbol.upper()
        price = get_share_price(symbol)
        if price <= 0:
            return False
            
        total_cost = price * quantity
        
        if total_cost > self.balance:
            return False
            
        # Deduct from balance
        self.balance -= total_cost
        
        # Update holdings
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
            
        # Record transaction
        self._record_transaction(
            transaction_type='buy',
            amount=total_cost,
            symbol=symbol,
            quantity=quantity
        )
        
        return True
    
    def sell_shares(self, symbol: str, quantity: int) -> bool:
        """
        Sell shares of a stock.
        
        Args:
            symbol: Stock symbol to sell
            quantity: Number of shares to sell
            
        Returns:
            bool: True if sale successful, False if insufficient shares
            
        Raises:
            ValueError: If quantity is not positive
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
            
        symbol = symbol.upper()
        
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            return False
            
        price = get_share_price(symbol)
        if price <= 0:
            return False
            
        total_revenue = price * quantity
        
        # Add to balance
        self.balance += total_revenue
        
        # Update holdings
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
            
        # Record transaction
        self._record_transaction(
            transaction_type='sell',
            amount=total_revenue,
            symbol=symbol,
            quantity=quantity
        )
        
        return True
    
    def _record_transaction(self, transaction_type: str, amount: float, 
                         symbol: str = None, quantity: int = None) -> None:
        """
        Record a transaction in the transaction history.
        
        Args:
            transaction_type: Type of transaction
            amount: Monetary amount
            symbol: Stock symbol (optional)
            quantity: Number of shares (optional)
        """
        transaction = {
            'datetime': datetime.datetime.now().isoformat(),
            'type': transaction_type,
            'symbol': symbol,
            'quantity': quantity,
            'amount': amount,
            'balance': self.balance
        }
        self.transactions.append(transaction)
    
    def calculate_portfolio_value(self) -> float:
        """
        Calculate total value of stock holdings.
        
        Returns:
            float: Total portfolio value
        """
        total_value = 0.0
        for symbol, quantity in self.holdings.items():
            price = get_share_price(symbol)
            total_value += price * quantity
        return total_value
    
    def compute_profit_or_loss(self) -> float:
        """
        Calculate profit or loss from initial deposit.
        
        Returns:
            float: Profit (positive) or loss (negative)
        """
        current_total = self.balance + self.calculate_portfolio_value()
        return current_total - self.initial_deposit
    
    def get_holdings_report(self) -> Dict[str, Dict[str, float]]:
        """
        Get detailed report of current holdings.
        
        Returns:
            dict: Holdings with quantity, price, and total value
        """
        report = {}
        for symbol, quantity in self.holdings.items():
            price = get_share_price(symbol)
            total_value = price * quantity
            report[symbol] = {
                'quantity': quantity,
                'current_price': price,
                'total_value': total_value
            }
        return report
    
    def get_transactions(self) -> List[Dict]:
        """
        Get all transactions.
        
        Returns:
            list: List of transaction dictionaries
        """
        return self.transactions.copy()
    
    def get_portfolio_summary(self) -> Dict[str, float]:
        """
        Get portfolio summary for display.
        
        Returns:
            dict: Portfolio summary with key metrics
        """
        return {
            'portfolio_value': self.calculate_portfolio_value(),
            'available_balance': self.balance,
            'total_profit_loss': self.compute_profit_or_loss()
        }
    
    @staticmethod
    def get_bond_interest_rates() -> Dict[str, float]:
        """
        Get current bond interest rates.
        
        Returns:
            dict: Bond maturities mapped to interest rates
        """
        return {
            '1-month': 0.5,
            '3-month': 0.75,
            '6-month': 1.0,
            '1-year': 1.5,
            '2-year': 2.0,
            '3-year': 2.5,
            '5-year': 3.0,
            '10-year': 3.5,
            '20-year': 4.0,
            '30-year': 4.5
        }
    
    @staticmethod
    def get_current_share_prices(symbols: List[str]) -> Dict[str, float]:
        """
        Get current prices for given symbols.
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            dict: Symbol to price mapping
        """
        prices = {}
        for symbol in symbols:
            prices[symbol.upper()] = get_share_price(symbol.upper())
        return prices