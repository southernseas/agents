# accounts.py Technical Documentation

## Overview
This module implements a simulated trading platform's account management system with user authentication, financial operations, and market data integration. It supports user registration/login, fund management, stock trading operations, and provides market data for simulation purposes.

## Key Components

### 1. Mock Share Price Provider
```python
def get_share_price(symbol: str) -> float
```
**Purpose:** Return simulated stock prices for demo trading  
**Parameters:**
- `symbol`: Stock ticker symbol (case-insensitive)
**Returns:** 
- Fixed prices for AAPL(150), TSLA(250), GOOGL(2700), default 100 for other symbols

### 2. Account Class
```python
class Account
```
**Purpose:** Represents user accounts with trading capabilities  
**Class Variables:**
- `_all_users`: Registry of all accounts by email

#### Core Methods:

##### User Management
```python
@classmethod register(email: str, password: str) -> Account
@classmethod login(email: str, password: str) -> Account
```
- Perform input validation and authentication
- Raise `ValueError` for invalid credentials or duplicate emails

##### Fund Management
```python
def deposit_funds(self, amount: float) -> None
def withdraw_funds(self, amount: float) -> None
```
- Enforce positive values and sufficient funds
- Record timestamped transactions in history

##### Trading Operations
```python
def buy_shares(self, symbol: str, quantity: int) -> None
def sell_shares(self, symbol: str, quantity: int) -> None
```
- Validate stock symbols and quantities
- Use `get_share_price()` for market price lookup
- Maintain holdings tracking and portfolio balances
- Generate detailed transaction records

##### Reporting Methods
```python
def get_transaction_history(self) -> List[Dict]
def get_holdings_summary(self) -> Dict[str, int]
def get_holdings_detail(self) -> List[Dict]
def get_profit_loss(self) -> float
def get_portfolio_value(self) -> float
```
- Provide current portfolio status and historical data
- Calculate market values using current share prices
- Show detailed holdings with real-time valuations

### 3. Market Data Accessors
```python
def get_current_share_prices() -> Dict[str, float]
def get_bond_interest_rates() -> Dict[str, float]
def get_currency_rates() -> Dict[str, float]
def get_latest_news() -> List[Dict]
```
**Purpose:** Provide simulated market reference data  
**Returns:**
- Fixed-rate implementations for share prices (AAPL/TSLA/GOOGL)
- Predefined interest rates for various bond terms (up to 30 years)
- Currency exchange rates (USD base)
- Mock news updates with timestamps

## Security Implementation
- Passwords stored in plaintext (in-memory demo only)
- Class-level registry with lookup validation
- Input validation for all operations
- Transaction history tracking for all financial activities

## State Management
All user data is stored in memory:
- User registry in `Account._all_users`
- Each Account maintains:
  - Current portfolio value
  - Holdings tracking
  - Transaction history
  - Initial deposit for P/L calculation

## Error Handling
All public methods raise `ValueError` with descriptive messages for:
- Invalid arguments
- Insufficient funds
- Insufficient holdings
- Existing email registrations
- Missing user credentials

## Example Usage
```python
# Create user
account = Account.register("user@example.com", "password123")

# Add funds
account.deposit_funds(10000)

# Buy stocks
account.buy_shares("AAPL", 5)

# View portfolio
print(f"Current Portfolio Value: {account.get_portfolio_value():.2f}")
```

## Technical Notes
1. Transaction history uses ISO 8601 timestamps
2. All currency values in USD
3. Holdings dictionary stores stock symbols as uppercase keys
4. Mock implementations intended for demo purposes only
5. No persistent storage integration