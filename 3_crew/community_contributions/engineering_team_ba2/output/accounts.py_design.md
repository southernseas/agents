# Detailed Design for accounts.py Module

## 1. Classes

### 1.1 `Account` Class
Manages user account operations, trading transactions, and financial calculations. All functionality is encapsulated in this single class.

**Attributes:**
```python
- username: str
- password: str
- email: str
- balance: float
- portfolio: Dict[str, int]  # {symbol: quantity_held}
- initial_deposit: float
- created_at: datetime.datetime
- transaction_history: List[Dict]  # List of all transactions
```

---

## 2. Methods

### 2.1 Class Constructor
```python
def __init__(self, username: str, password: str, email: str, initial_deposit: float)
```
- Creates a new account with base fields initialized
- Validates password format (must be >8 chars)
- Sets `initial_deposit` as baseline for profit/loss calculations
- Initializes empty portfolio dictionary

---

### 2.2 Account Management
```python
def login(self, username: str, password: str) -> None
```
- Validates username/password against stored credentials
- Raises `AuthenticationError` for invalid credentials

```python
def validate_password(password: str) -> None
```
- Static method for password format validation
- Enforces length, complexity

```python
def set_password(self, new_password: str) -> None
```
- Updates password with validation
- Requires current password
- Raises `AuthenticationError` if invalid

---

### 2.3 Balance Management
```python
def deposit(self, amount: float) -> None
```
- Adds funds to account balance
- Logs transaction
- Raises `ValueError` for non-positive amounts

```python
def withdraw(self, amount: float) -> None
```
- Subtracts funds from balance
- Validates against available balance
- Raises `InsufficientFundsError` if negative balance would occur

```python
def get_balance(self) -> float
```
- Returns current account balance

---

### 2.4 Trading Operations
```python
def buy_shares(self, symbol: str, quantity: int) -> None
```
- Calculate cost using `get_share_price()`
- Validates sufficient funds
- Adds shares to portfolio (increment if already held)
- Logs transaction
- Raises:
  - `ShareNotFoundError` for invalid symbols
  - `InsufficientFundsError` for insufficient balance

```python
def sell_shares(self, symbol: str, quantity: int) -> None
```
- Validates owned shares count
- Removes shares from portfolio (subtract from quantity)
- Adds proceeds to balance
- Logs transaction
- Raises:
  - `ShareNotFoundError` for invalid symbols
  - `InvalidQuantityError` for quantities exceeding holdings

```python
def calculate_trade_value(symbol: str, quantity: int) -> float
```
- Static helper method to compute trade value
- Uses `get_share_price()`

---

### 2.5 Portfolio Management
```python
def calculate_portfolio_value(self) -> float
```
- Sum value of all holdings using `get_share_price()`
- Adds cash balance for total portfolio value

```python
def calculate_profit_loss(self) -> float
```
- Computes difference between current value and initial deposit
- Returns positive/profit or negative/loss amount

```python
def get_holdings(self) -> List[Dict]
```
- Returns list of owned shares with:
  - symbol
  - quantity
  - current price (from `get_share_price()`)
  - total value

```python
def get_transaction_history(self) -> List[Dict]
```
- Returns all logged transactions with:
  - timestamp
  - transaction type
  - symbol
  - quantity
  - amount
  - balance after transaction

---

### 2.6 Financial Reports
```python
def generate_profit_loss_report(self) -> Dict
```
- Returns dictionary with:
  - total deposits
  - total withdrawals
  - net change from trading
  - current profit/loss

```python
def get_account_summary(self) -> Dict
```
- Returns comprehensive summary including:
  - account balance
  - portfolio value
  - profit/loss percentage
  - all holdings with details

---

### 2.7 External Integrations
```python
def get_share_price(symbol: str) -> float
```
- Static method with test implementation:
  ```python
  FIXED_PRICES = {
      'AAPL': 190.0,
      'TSLA': 250.0,
      'GOOGL': 125.0
  }
  return FIXED_PRICES.get(symbol, 0)
  ```

```python
def get_interest_rates() -> Dict
```
- Static method with test implementation:
  ```python
  return {
      '1-month': 0.5,
      '3-month': 0.75,
      '6-month': 1.0,
      '1-year': 1.5,
      ...
      '30-year': 4.2
  }
  ```

---

## 3. Error Classes
All exceptions are defined in the Account class:
```python
class AuthenticationError(Exception): ...
class InsufficientFundsError(Exception): ...
class InvalidQuantityError(Exception): ...
class ShareNotFoundError(Exception): ...
class TransactionValidationError(Exception): ...
class CurrencyExchangeError(Exception): ...
```

---

## 4. Transaction Log Format
Each transaction stored as dictionary with:
```python
{
    'type': 'deposit' | 'withdraw' | 'buy' | 'sell',
    'timestamp': datetime.datetime,
    'symbol': str,
    'quantity': int, 
    'amount': float,
    'total_value': float,
    'remaining_balance': float
}
```

---

This design provides a complete, self-contained account management system that meets all specified requirements. The class handles authentication, financial transactions, portfolio management, reporting, and integrates with required external systems while maintaining data consistency and security.