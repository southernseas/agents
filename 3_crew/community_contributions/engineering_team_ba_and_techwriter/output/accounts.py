import datetime
from typing import Dict, List

# Mock implementation of get_share_price for testing
def get_share_price(symbol: str) -> float:
    """Mock implementation for testing - returns fixed prices for certain stocks"""
    prices = {
        "AAPL": 150.0,
        "TSLA": 250.0,
        "GOOGL": 2700.0
    }
    return prices.get(symbol.upper(), 100.0)

class Account:
    """Account class for managing user accounts in a trading simulation platform."""
    
    # Class-level storage for all registered users
    _all_users: Dict[str, 'Account'] = {}
    
    def __init__(self, email: str, password: str):
        """Initialize a new account."""
        self.email = email
        self.password = password
        self.funds = 0.0
        self.initial_deposit = 0.0
        self.holdings: Dict[str, int] = {}
        self.transaction_history: List[Dict] = []
    
    @classmethod
    def register(cls, email: str, password: str) -> 'Account':
        """Create a new user account."""
        if email in cls._all_users:
            raise ValueError(f"Email {email} already exists")
        
        user = cls(email, password)
        cls._all_users[email] = user
        return user
    
    @classmethod
    def login(cls, email: str, password: str) -> 'Account':
        """Authenticate a user by email and password."""
        if email not in cls._all_users:
            raise ValueError("User not found")
        
        user = cls._all_users[email]
        if user.password != password:
            raise ValueError("Invalid password")
        
        return user
    
    def deposit_funds(self, amount: float) -> None:
        """Add funds to the account."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        if self.initial_deposit == 0:
            self.initial_deposit = amount
        
        self.funds += amount
        
        self.transaction_history.append({
            "type": "deposit",
            "amount": amount,
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    def withdraw_funds(self, amount: float) -> None:
        """Withdraw funds from the account."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        if self.funds < amount:
            raise ValueError("Insufficient funds")
        
        self.funds -= amount
        
        self.transaction_history.append({
            "type": "withdrawal",
            "amount": amount,
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    def buy_shares(self, symbol: str, quantity: int) -> None:
        """Buy shares of a given symbol."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        symbol = symbol.upper()
        current_price = get_share_price(symbol)
        total_cost = current_price * quantity
        
        if self.funds < total_cost:
            raise ValueError(
                f"Insufficient funds to purchase {quantity} shares of {symbol} "
                f"at ${current_price} each. Available: ${self.funds}"
            )
        
        # Execute the transaction
        self.funds -= total_cost
        
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        
        self.transaction_history.append({
            "type": "buy",
            "symbol": symbol,
            "quantity": quantity,
            "price": current_price,
            "total_cost": total_cost,
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    def sell_shares(self, symbol: str, quantity: int) -> None:
        """Sell shares of a given symbol."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        symbol = symbol.upper()
        
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError(
                f"Insufficient holdings to sell {quantity} shares of {symbol}. "
                f"Current holdings: {self.holdings.get(symbol, 0)}"
            )
        
        current_price = get_share_price(symbol)
        total_value = current_price * quantity
        
        # Execute the transaction
        self.funds += total_value
        self.holdings[symbol] -= quantity
        
        # Remove symbol from holdings if quantity reaches zero
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        
        self.transaction_history.append({
            "type": "sell",
            "symbol": symbol,
            "quantity": quantity,
            "price": current_price,
            "total_value": total_value,
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    def get_transaction_history(self) -> List[Dict]:
        """Return the list of all user transactions."""
        return self.transaction_history.copy()
    
    def get_holdings_summary(self) -> Dict[str, int]:
        """Return a summary of current holdings."""
        return self.holdings.copy()
    
    def get_holdings_detail(self) -> List[Dict]:
        """Return detailed holdings including current value."""
        details = []
        for symbol, quantity in self.holdings.items():
            current_price = get_share_price(symbol)
            current_value = current_price * quantity
            details.append({
                "symbol": symbol,
                "quantity": quantity,
                "current_price": current_price,
                "current_value": current_value
            })
        return details
    
    def get_profit_loss(self) -> float:
        """Compute profit/loss as the difference between current portfolio value and initial deposit."""
        return self.get_portfolio_value() - self.initial_deposit
    
    def get_portfolio_value(self) -> float:
        """Return the total value of the user's portfolio (cash + value of all holdings)."""
        return self.funds + self.get_holdings_value()
    
    def get_holdings_value(self) -> float:
        """Return the aggregated market value of all holdings."""
        total_value = 0.0
        for symbol, quantity in self.holdings.items():
            current_price = get_share_price(symbol)
            total_value += current_price * quantity
        return total_value

# Additional functions for UI screens (as mentioned in requirements)

def get_current_share_prices() -> Dict[str, float]:
    """Get current prices for all available shares."""
    symbols = ["AAPL", "TSLA", "GOOGL"]
    return {symbol: get_share_price(symbol) for symbol in symbols}

def get_bond_interest_rates() -> Dict[str, float]:
    """Get current bond interest rates."""
    return {
        "1-month": 0.05,
        "3-month": 0.06,
        "6-month": 0.07,
        "1-year": 0.08,
        "2-year": 0.09,
        "3-year": 0.10,
        "5-year": 0.12,
        "10-year": 0.15,
        "20-year": 0.18,
        "30-year": 0.20
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
        "CNY": 6.45
    }

def get_latest_news() -> List[Dict]:
    """Get latest news (mock implementation)."""
    return [
        {
            "title": "Market Hits All-Time High",
            "summary": "Major indices reach record levels amid strong earnings...",
            "timestamp": datetime.datetime.now().isoformat()
        },
        {
            "title": "Tech Stocks Rally",
            "summary": "Technology sector leads gains with AAPL and TSLA outperforming...",
            "timestamp": datetime.datetime.now().isoformat()
        }
    ]