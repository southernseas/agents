# Detailed Design for `accounts.py` Module

## Overview
The `accounts.py` module defines the `Account` class for managing user accounts in a trading simulation platform. The class encapsulates user registration, authentication, funds management, trading transactions, portfolio tracking, and transaction history. The module integrates with external functions like `get_share_price(symbol)` for real-time share price retrieval.

---

## Classes and Functions

### Class: `Account`
Singleton per user, representing a user account and managing financial operations.

#### Class-level Attributes
- `_all_users`: Dictionary to store all registered users ({`email`: `Account` instance}).

#### Instance Attributes
- `email`: str - unique email identifier.
- `password`: str - secure user password (stored in plaintext for this design; note: in production, this should be hashed).
- `funds`: float - available balance for trading.
- `initial_deposit`: float - user's first deposit (for profit/loss calculations).
- `holdings`: Dict[str, int] - mapping from stock symbols to owned quantities (e.g., `{"AAPL": 500}`).
- `transaction_history`: List[Dict] - list of all transactions (buy/sell) with metadata.

---

### Methods

#### Static/Class Methods
- **`register(email: str, password: str) -> Account`**
  Creates a new user account, validates email uniqueness, and initializes balances/holdings.
  - Raises `ValueError` if the email already exists.

- **`login(email: str, password: str) -> Account`**
  Authenticates a user by email/password and returns the corresponding `Account` instance.
  - Raises `ValueError` for invalid credentials or non-existent user.

#### Instance Methods
- **`deposit_funds(amount: float) -> None`**
  Adds specified amount to user's funds.
  - Raises `ValueError` if amount is non-positive.

- **`withdraw_funds(amount: float) -> None`**
  Deducts funds while ensuring the balance does not go negative.
  - Raises `ValueError` if insufficient funds.

- **`buy_shares(symbol: str, quantity: int) -> None`**
  Validates available balance and share price, then executes a purchase.
  - Uses `get_share_price(symbol)` to fetch current market price.
  - Raises `ValueError` for insufficient funds.

- **`sell_shares(symbol: str, quantity: int) -> None`**
  Validates ownership of shares before selling and updates balance.
  - Raises `ValueError` for insufficient holdings.

- **`get_transaction_history() -> List[Dict]`**
  Returns the list of all user transactions with details (timestamp, type, quantity, etc.).

- **`get_holdings_summary() -> Dict[str, int]`**
  Returns a summary of current holdings (e.g., `{"AAPL": 400, "TSLA": 200}`).

- **`get_holdings_detail() -> List[Dict]`**
  Returns detailed holdings including current value:
  ```python
  [
    {"symbol": "AAPL", "quantity": 400, "current_price": 150.0, "current_value": 60000.0}, 
    ...
  ]
  ```

- **`get_profit_loss() -> float`**
  Computes profit/loss as the difference between current portfolio value and the initial deposit.

- **`get_portfolio_value() -> float`**
  Returns the total value of the user's portfolio (cash + value of all holdings).

- **`get_holdings_value() -> float`**
  Returns the aggregated market value of all holdings.

---

### Validation Rules
1. **Withdrawals**: Ensures `funds >= amount`.
2. **Purchases**: Validates that `funds >= cost = quantity * get_share_price(symbol)`.
3. **Sales**: Validates that ownership quantity is sufficient.
4. **Funds and Transactions**: Ensures atomic updates (e.g., both `holdings` and `funds` are updated or rolled back in case of errors).

---

### Error Handling
- All operations raise `ValueError` with descriptive messages for invalid inputs or insufficient resources.
- Example error: `ValueError("Insufficient funds to purchase 150 shares of AAPL at $250 each")`.

---

### Assumptions and Notes
1. **External Integration**: Relies on a tested `get_share_price(symbol)` function for real-time or fixed testing prices.
2. **Security**: Passwords are stored in plaintext, but real-world systems would require encryption or hashing.
3. **UI Separation**: This module provides data and logic support for the UI screens (e.g., "portfolio" or "profit/loss") but does not implement UI components.
4. **Atomicity**: All operations ensure transaction-like behavior to maintain data integrity.

---

#### Example Usage
```python
user1 = Account.register("alice@example.com", "securePass123")
user1.deposit_funds(10000)
user1.buy_shares("AAPL", 100)  # Assumes get_share_price("AAPL") = 150
assert user1.get_profit_loss() == (user1.get_portfolio_value() - 10000)
```

This design ensures a self-contained, testable `Account` system that meets all required functional and validation criteria.