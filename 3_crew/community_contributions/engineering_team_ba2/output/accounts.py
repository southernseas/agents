import hashlib
import datetime
from typing import Dict, List, Optional

class Transaction:
    """Represents a single stock transaction (buy or sell)."""
    
    def __init__(self, symbol: str, quantity: int, transaction_type: str, timestamp: datetime.datetime):
        self.symbol = symbol
        self.quantity = quantity
        self.transaction_type = transaction_type
        self.timestamp = timestamp
    
    def __repr__(self) -> str:
        action = "Bought" if self.transaction_type == "buy" else "Sold"
        return f"{action} {self.quantity} shares of {self.symbol} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


def get_share_price(symbol: str) -> float:
    """Mock implementation for development/testing returns fixed prices."""
    prices = {
        "AAPL": 150.0,
        "TSLA": 180.0,
        "GOOGL": 2800.0,
    }
    return prices.get(symbol.upper(), 0.0)


class Account:
    """Represents a user's trading account with funds, holdings, and transaction history."""
    
    # Class variable to store all accounts
    _accounts: Dict[str, 'Account'] = {}
    
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        # Simple hash for demonstration (use bcrypt in production)
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.balance = 0.0
        self.initial_deposit = 0.0
        self.holdings: Dict[str, int] = {}
        self.transactions: List[Transaction] = []
    
    @classmethod
    def register(cls, username: str, email: str, password: str) -> bool:
        """Register a new account."""
        if not username or not email or not password:
            raise ValueError("Username, email, and password are required")
        
        # Check if username or email already exists
        for account in cls._accounts.values():
            if account.username == username:
                raise ValueError("Username already exists")
            if account.email == email:
                raise ValueError("Email already registered")
        
        new_account = cls(username, email, password)
        cls._accounts[username] = new_account
        return True
    
    @classmethod
    def login(cls, username_or_email: str, password: str) -> Optional['Account']:
        """Login with username or email and password."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Try to find by username
        if username_or_email in cls._accounts:
            account = cls._accounts[username_or_email]
            if account.password_hash == password_hash:
                return account
        
        # Try to find by email
        for account in cls._accounts.values():
            if account.email == username_or_email and account.password_hash == password_hash:
                return account
        
        return None
    
    def deposit_funds(self, amount: float) -> None:
        """Deposit funds into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount
        if self.initial_deposit == 0:
            self.initial_deposit = amount
    
    def withdraw_funds(self, amount: float) -> None:
        """Withdraw funds from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if self.balance < amount:
            raise ValueError("Insufficient funds for withdrawal")
        
        self.balance -= amount
    
    def buy_stock(self, symbol: str, quantity: int) -> None:
        """Buy shares of a stock."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        price = get_share_price(symbol.upper())
        if price <= 0:
            raise ValueError("Invalid stock symbol")
        
        total_cost = price * quantity
        if self.balance < total_cost:
            raise ValueError("Insufficient funds to buy shares")
        
        # Update balance and holdings
        self.balance -= total_cost
        symbol = symbol.upper()
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        
        # Record transaction
        transaction = Transaction(symbol, quantity, "buy", datetime.datetime.now())
        self.transactions.append(transaction)
    
    def sell_stock(self, symbol: str, quantity: int) -> None:
        """Sell shares of a stock."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        symbol = symbol.upper()
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError("Insufficient shares to sell")
        
        price = get_share_price(symbol)
        if price <= 0:
            raise ValueError("Invalid stock symbol")
        
        total_proceeds = price * quantity
        
        # Update balance and holdings
        self.balance += total_proceeds
        self.holdings[symbol] -= quantity
        
        # Remove symbol from holdings if quantity reaches 0
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        
        # Record transaction
        transaction = Transaction(symbol, quantity, "sell", datetime.datetime.now())
        self.transactions.append(transaction)
    
    def calculate_portfolio_value(self) -> float:
        """Calculate total portfolio value (cash + stock holdings)."""
        stock_value = 0.0
        for symbol, quantity in self.holdings.items():
            stock_value += get_share_price(symbol) * quantity
        
        return self.balance + stock_value
    
    def calculate_profit_loss(self) -> float:
        """Calculate profit or loss from initial deposit."""
        if self.initial_deposit == 0:
            return 0.0
        
        return self.calculate_portfolio_value() - self.initial_deposit
    
    def get_holdings(self) -> Dict[str, int]:
        """Get current stock holdings."""
        return self.holdings.copy()
    
    def get_transaction_history(self) -> List[Transaction]:
        """Get transaction history."""
        return self.transactions.copy()


# Additional helper functions for UI screens

def get_current_share_prices() -> Dict[str, float]:
    """Get current share prices for all supported stocks."""
    return {
        "AAPL": get_share_price("AAPL"),
        "TSLA": get_share_price("TSLA"),
        "GOOGL": get_share_price("GOOGL"),
    }


def get_bond_interest_rates() -> Dict[str, float]:
    """Get current bond interest rates."""
    return {
        "1-month": 0.05,
        "3-month": 0.10,
        "6-month": 0.25,
        "1-year": 0.50,
        "2-year": 1.00,
        "3-year": 1.50,
        "5-year": 2.00,
        "10-year": 2.50,
        "20-year": 3.00,
        "30-year": 3.50,
    }


def get_currency_rates() -> Dict[str, float]:
    """Get current currency exchange rates (USD as base)."""
    return {
        "USD": 1.0,
        "EUR": 0.85,
        "GBP": 0.73,
        "JPY": 110.0,
        "CAD": 1.25,
        "AUD": 1.35,
        "CHF": 0.92,
    }


def get_latest_news() -> List[str]:
    """Get latest financial news headlines."""
    return [
        "Tech stocks rally on strong earnings reports",
        "Federal Reserve signals potential rate changes",
        "Oil prices surge amid global supply concerns",
        "Cryptocurrency market sees renewed investor interest",
        "Major indices reach new all-time highs",
    ]