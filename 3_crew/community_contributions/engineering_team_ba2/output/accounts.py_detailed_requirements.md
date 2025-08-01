```markdown
# Detailed Requirements for the Trading Simulation Platform Account Management System

1. User Account Management
   1.1. Account Creation
       - The system shall allow a new user to create an account.
       - The user must provide the required registration details (e.g., username, password, email) during account creation.
   1.2. User Authentication
       - The system shall provide a user login screen for authentication.
       - Appropriate error messages shall be displayed for an invalid username/password.
   1.3. Account Balance Management
       - The system shall allow a user to deposit funds into their account.
       - The system shall allow a user to withdraw funds from their account.
       - The system shall validate transactions to ensure that withdrawals do not result in a negative balance.

2. Trading Transactions
   2.1. Buy/Sell Share Recording
       - The system shall allow users to record transactions where they buy or sell shares.
       - Each transaction must capture the following details:
           • Transaction type (buy or sell)
           • Share symbol (e.g., AAPL, TSLA, GOOGL)
           • Quantity of shares bought or sold
           • Transaction timestamp.
   2.2. Transaction Validation
       - For buy transactions:
           • The system shall verify that the user has sufficient funds to cover the purchase based on the current share price.
       - For sell transactions:
           • The system shall verify that the user holds enough shares in their portfolio to complete the sell order.
           • If the user attempts to sell more shares than owned, the system should reject the transaction with an appropriate error message.

3. Portfolio Management and Reporting
   3.1. Portfolio Valuation
       - The system shall calculate the total value of the user's portfolio.
           • The valuation is computed by summing the current market value of each share held (using get_share_price(symbol) for current price lookup).
       - The system shall calculate the profit or loss relative to the initial deposit.
   3.2. Holdings Reporting
       - The system shall provide a “Holdings” screen that displays the details of current share holdings at any point in time.
       - The report shall include share symbol, total quantity held, current market price, and total value per share type.
   3.3. Profit or Loss Reporting
       - The system shall provide a “Profit or Loss” screen that displays the current profit or loss for the user.
       - The calculation shall compare the current total portfolio value against the initial deposit (or cumulative net deposits) and all executed transactions.
   3.4. Transaction History Reporting
       - The system shall maintain a complete log of all transactions (deposits, withdrawals, buy orders, sell orders).
       - The system shall provide a “Transactions” screen that lists all transactions in chronological order, with details (date/time, type, share symbol, quantity, and amount).

4. Business Rules and Restrictions
   4.1. Withdrawal Restrictions
       - The system shall prevent a withdrawal if it would result in a negative balance.
   4.2. Buy Transaction Restrictions
       - The system shall prevent users from buying shares if their available funds are insufficient based on the current share price.
   4.3. Sell Transaction Restrictions
       - The system shall prevent users from selling more shares than they currently hold.
   
5. Integration with External Functions
   5.1. Share Price Retrieval
       - The system shall utilize the function get_share_price(symbol) to retrieve the current price for a given share symbol.
       - A test implementation of get_share_price(symbol) will return fixed prices for AAPL, TSLA, and GOOGL.
   5.2. Bond Interest Rates Data
       - The system shall have a mechanism to display current bond interest rates.
       - The “Bond Interest Rates” screen must support viewing the following bonds:
           • 1-month, 3-month, 6-month, 1-year, 2-year, 3-year, 5-year, 10-year, 20-year, and 30-year.

6. User Interface Screens
   6.1. Login Screen
       - Provide a screen where users can enter their credentials to log in.
   6.2. Current Share Price Screen
       - Display the current share price information using get_share_price(symbol) for available shares.
   6.3. Bond Interest Rates Screen
       - Display current bond interest rates for the specified bond durations.
   6.4. Transactions Screen
       - Display the user’s complete transaction history (deposits, withdrawals, buys, and sells).
   6.5. Portfolio Screen
       - Display an overview of the user’s portfolio including current holdings and total portfolio value.
   6.6. Profit or Loss Screen
       - Display the user’s calculated profit or loss at any point in time.
   6.7. Holdings Screen
       - Present detailed information on share holdings, similar to the portfolio screen (if differentiated from portfolio, both should be maintained).
   6.8. Currency Exchange Screen
       - Allow the user to exchange one currency for another as per current currency exchange rates.
       - Validate exchange transactions with proper conversion and sufficient funds.
   6.9. News Screen
       - Provide a screen to display the latest market news and trading-related updates.
   6.10. Currency Rates Screen
       - Show the current currency exchange rates for various currencies.

7. General System Considerations
   7.1. Data Consistency
       - Ensure that all account, transaction, and portfolio data remains consistent across sessions.
   7.2. Error Handling and Feedback
       - Provide clear error messages and confirmation dialogues for all user actions (e.g., attempting an invalid transaction).
   7.3. Security
       - Implement secure login procedures and session management to protect user information.
   7.4. Scalability
       - Design the system components to allow potential future expansion of trading functions and market data sources.

This document will serve as the detailed requirements handoff to the engineering lead, ensuring a comprehensive implementation that meets all the business needs.
```