------------------------------------------------------------
# Detailed Design for accounts.py Module

This document provides a detailed design for the trading simulation platform’s account management system. The entire implementation is encapsulated within one Python module, "accounts.py", which includes the main class `Account`. This module is self-contained and will support authentication, funds management, transaction recording, portfolio calculations, and integration with market data functions.

---

## Module: accounts.py

### Overview
- **Purpose:** Provide user account management including registration, authentication, funds deposit/withdrawal, transaction records, portfolio and holdings calculations, and data retrieval for UI screens.
- **Integration:** The module integrates with the supplied function `get_share_price(symbol)` to obtain current share prices for specified stocks (AAPL, TSLA, and GOOGL).

---

## Class: Account

### Attributes
- **username (str):** Unique identifier for the user.
- **email (str):** Email address of the user; will be validated for format.
- **password (str):** Account password (enforced with complexity rules). (In a real implementation, a hash should be stored.)
- **balance (float):** Current available funds in the account.
- **initial_deposit (float):** The initial amount deposited into the account used for profit/loss computation.
- **holdings (dict):** Dictionary mapping share symbols to quantities held.
- **transactions (list):** A list of dictionary objects containing transaction details (date/time, type, share symbol if applicable, quantity, amount, and resulting balance).
- **session (dict or object):** Representation of the user session for authentication; can include a session token, expiry, etc.

### Initialization and User Registration
- **Method:** `__init__(username: str, email: str, password: str)`
  - **Description:** Creates a new account instance with the given username, email, and password. Initializes balance to zero, holdings as an empty dictionary, and transactions list as empty.
  - **Validations:**
    - Verify email address format.
    - Enforce password complexity.
  
- **Method:** `register_account()`
  - **Description:** Handles the registration process. May include additional steps such as sending registration confirmation and storing user data in a persistent store.
  - **Parameters:** None (uses object’s attributes).
  - **Return:** Success or error status.

- **Method:** `login(password: str) -> bool`
  - **Description:** Authenticates the user by comparing the provided password with the stored password.
  - **Parameters:** 
    - `password`: The password input for verification.
  - **Return:** Boolean value indicating success (True) or failure (False).
  - **Notes:** Secure session management should be initiated on successful login.

---

## Funds Management

### Deposit Funds
- **Method:** `deposit_funds(amount: float) -> None`
  - **Description:** Allows the user to deposit funds into their account.
  - **Parameters:**
    - `amount`: The deposit amount (must be a positive number).
  - **Functionality:**
    - Update the account balance.
    - Record the deposit transaction including the deposit amount, timestamp, and resulting balance.
    - If this is the first deposit, store it as the initial deposit.

### Withdraw Funds
- **Method:** `withdraw_funds(amount: float) -> bool`
  - **Description:** Enables the user to withdraw funds from their account.
  - **Parameters:**
    - `amount`: The withdrawal amount (must be positive).
  - **Functionality:**
    - Validate that withdrawal does not result in a negative balance.
    - Update the account balance if validation passes.
    - Record the withdrawal transaction (withdrawal amount, timestamp, and new balance).
  - **Return:** Boolean value indicating whether the withdrawal was successful.
  - **Business Rule:** Prevent negative account balances.

---

## Transaction Management

### Recording Transactions
- **Method:** `record_transaction(transaction_type: str, amount: float, symbol: str = None, quantity: int = None) -> None`
  - **Description:** Appends a new transaction object into the transaction history.
  - **Parameters:**
    - `transaction_type`: Type of transaction ("buy", "sell", "deposit", "withdrawal").
    - `amount`: The monetary amount involved in the transaction.
    - `symbol` (optional): Share symbol for buy/sell transactions.
    - `quantity` (optional): Number of shares bought or sold.
  - **Functionality:**
    - Record date/time, transaction type, share symbol (if applicable), quantity, amount, and resulting balance.
  
### Buying Shares
- **Method:** `buy_shares(symbol: str, quantity: int) -> bool`
  - **Description:** Processes the purchase of shares.
  - **Parameters:**
    - `symbol`: The stock symbol.
    - `quantity`: Number of shares to buy.
  - **Functionality:**
    - Retrieve current share price via `get_share_price(symbol)`.
    - Calculate total cost = current share price * quantity.
    - Validate that available funds are sufficient (prevent overbuy).
    - Deduct the total cost from the balance.
    - Update holdings by increasing the quantity for the given share symbol.
    - Record the buy transaction including details of share symbol, quantity, cost, and timestamp.
  - **Return:** Boolean indicating success or failure.

### Selling Shares
- **Method:** `sell_shares(symbol: str, quantity: int) -> bool`
  - **Description:** Processes selling shares.
  - **Parameters:**
    - `symbol`: The stock symbol.
    - `quantity`: Number of shares to sell.
  - **Functionality:**
    - Ensure that the quantity to sell does not exceed the shares currently held (prevent oversell).
    - Retrieve current share price using `get_share_price(symbol)`.
    - Calculate revenue = current share price * quantity.
    - Increase the account balance by the revenue amount.
    - Deduct the quantity from holdings.
    - Record the sell transaction including share symbol, quantity, revenue, date/time, and resulting balance.
  - **Return:** Boolean indicating success or failure.

---

## Portfolio and Holdings Calculation

### Portfolio Value Calculation
- **Method:** `calculate_portfolio_value() -> float`
  - **Description:** Computes the total value of the user's stock holdings.
  - **Functionality:**
    - For each share symbol in holdings, retrieve the current share price from `get_share_price(symbol)`.
    - Multiply each share's current price by the quantity held.
    - Sum all such values.
  - **Return:** Total portfolio value as a float.

### Profit or Loss Computation
- **Method:** `compute_profit_or_loss() -> float`
  - **Description:** Calculates the profit or loss against the initial deposit.
  - **Functionality:**
    - Compute total current value = account balance + portfolio value.
    - Subtract the initial_deposit from the total current value.
  - **Return:** Profit/loss value as a float.

### Holdings Reporting
- **Method:** `get_holdings_report() -> dict`
  - **Description:** Returns detailed information about the current holdings.
  - **Functionality:**
    - For each share symbol, include:
      - Quantity held.
      - Current share price (via `get_share_price(symbol)`).
      - Total value per holding (price * quantity).
  - **Return:** A dictionary mapping share symbols to their detailed holding information.

---

## Display and Reporting Related Methods
*(These methods provide data to the UI layer. They abstract the backend information into structured formats for display screens.)*

### Transaction Screen Data
- **Method:** `get_transactions() -> list`
  - **Description:** Returns the list of all transactions recorded by the account.
  - **Output Format:** Each transaction includes date/time, type (buy, sell, deposit, withdrawal), share symbol (if applicable), quantity, amount, and resulting balance.

### Portfolio Screen Data
- **Method:** `get_portfolio_summary() -> dict`
  - **Description:** Provides a summary of the portfolio.
  - **Functionality:**
    - Total portfolio value.
    - Available account balance.
    - Overall profit or loss computed.
  - **Return:** Dictionary containing portfolio summary details.

### Bond Interest Rates Screen Data
- **Method:** `get_bond_interest_rates() -> dict`
  - **Description:** Returns fixed or fetched bond interest rates for bonds with maturities: 1-month, 3-month, 6-month, 1-year, 2-year, 3-year, 5-year, 10-year, 20-year, and 30-year.
  - **Return:** A dictionary mapping bond maturities to their respective interest rates.
  - **Notes:** For testing, fixed sample values can be used.

### Current Share Price Screen Data
- **Method:** `get_current_share_prices(symbols: list) -> dict`
  - **Description:** Retrieves the current share price for each symbol provided.
  - **Parameters:**
    - `symbols`: List of stock symbols.
  - **Return:** Dictionary mapping each symbol to its current share price via `get_share_price(symbol)`.

---

## Integration Function

### get_share_price(symbol: str) -> float
- **Description:** Provided function that returns the current share price for a given stock symbol.
- **Specifics:**
  - Must return fixed prices for AAPL, TSLA, and GOOGL when testing.
  - Can be implemented within this module for testing purposes, or imported if provided externally.
- **Parameters:**
  - `symbol`: Stock symbol for which the price is requested.
- **Return:** A float representing the current price of the stock.

---

## Data Integrity and Business Rules Enforcement

- **Negative Balance Prevention:** The `withdraw_funds()` method ensures that a withdrawal does not cause the balance to fall below zero.
- **Overbuy Prevention:** The `buy_shares()` method validates that the account’s available funds are sufficient to cover the total cost of the purchase.
- **Oversell Prevention:** The `sell_shares()` method checks that the user holds enough shares before permitting sale.

---

## User Interface and Navigation Data Methods

Although the module is backend-focused, it supports the following UI-related functionalities to integrate with various screens:
- **Login Screen:** Data is provided via the `login()` method.
- **Current Share Price Screen:** Data provided by `get_current_share_prices()`.
- **Bond Interest Rates Screen:** Data provided by `get_bond_interest_rates()`.
- **Transactions Screen:** Data provided by `get_transactions()`.
- **Portfolio and Holdings Screens:** Data provided by `get_portfolio_summary()` and `get_holdings_report()`.
- **Profit or Loss Screen:** Data computed and provided by `compute_profit_or_loss()`.

The module is designed to be responsive to calls from a UI layer that can trigger periodic refreshes (e.g., using polling or push notifications) for market data such as share prices and bond interest rates.

---

## Data Persistence and Security Considerations

- **Data Persistence:** Although specifics are abstracted from this design, consider integrating with a database or another persistent storage mechanism to save user data, transactions, and holdings.
- **Security:** Ensure sensitive user information (passwords, session tokens) is handled securely. Use encryption and hashing where appropriate, and ensure secure communication channels between UI and backend.
- **Error Handling:** Each method should include appropriate error handling and logging to maintain data integrity and ease debugging.

---

This detailed design outlines the primary classes, methods, parameters, and functionalities required for implementing the backend module "accounts.py". It directly maps the detailed requirements to the classes and functions to guide the development and testing phases of the project.