1. User Account and Authentication
   1.1. Account Creation:  
       - The system shall provide a registration interface for new users to create an account.  
       - Required fields include username, email, and password.  
       - The system shall validate the format of the email and enforce password complexity rules.  
   1.2. User Login:  
       - The system shall provide a user login screen where registered users can log into their account using their credentials.  
       - Ensure secure authentication with appropriate session management.

2. Funds Management
   2.1. Deposit Funds:  
       - The system shall allow users to deposit funds into their account.  
       - Deposit operations must be recorded with the deposit amount, date, and resulting balance.
   2.2. Withdraw Funds:  
       - The system shall allow users to withdraw funds from their account.  
       - The system must prevent any withdrawal that would result in a negative account balance.  
       - All withdrawal transactions must be recorded with the withdrawal amount, date, and resulting balance.

3. Transaction Management
   3.1. Recording Transactions:  
       - The system shall allow users to record transactions indicating that they have bought or sold shares.  
       - Each transaction must capture the following details: action type (buy/sell), share symbol, quantity, and timestamp.  
       - The system shall maintain a detailed list of all transactions performed by the user over time.
   3.2. Transaction Validation:  
       - When buying shares, the system shall verify that the user’s available funds are sufficient to cover the cost of the intended purchase.  
       - When selling shares, the system shall verify that the user owns the shares in sufficient quantity to cover the sale.

4. Portfolio and Holdings Calculation
   4.1. Portfolio Value Calculation:  
       - The system shall calculate the total value of the user's portfolio by summing up the current value of all held shares.  
       - The current share price for each stock will be determined using the provided function get_share_price(symbol).  
       - The test implementation of get_share_price(symbol) should return fixed prices for AAPL, TSLA, and GOOGL.
   4.2. Profit or Loss Computation:  
       - The system shall compute the profit or loss from the user's initial deposit.  
       - The calculation must take into account the current portfolio value versus the initial funds deposited.
   4.3. Holdings Reporting:  
       - The system shall be able to report the current holdings of the user at any point in time.  
       - The holdings display should include share symbols, quantities held, and the current value per holding.

5. Display and Reporting Screens
   5.1. Login Screen:  
       - A dedicated screen that allows users to log into the system.
   5.2. Current Share Price Screen:  
       - A screen that displays the current share prices for available stocks using the get_share_price(symbol) function.
   5.3. Bond Interest Rates Screen:  
       - A screen that displays the current bond interest rates for the following bonds: 1-month, 3-month, 6-month, 1-year, 2-year, 3-year, 5-year, 10-year, 20-year, and 30-year.
   5.4. Transactions Screen:  
       - A screen that lists all transactions that the user has made over time.  
       - The data should include date/time, transaction type (buy/sell/deposit/withdrawal), share symbol (if applicable), quantity, and amount.
   5.5. Portfolio and Holdings Screens:  
       - A portfolio screen that displays the overall holdings of the user including the total current value.
       - A separate (or integrated) holdings screen should provide detailed information on each type of asset held.
       - A profit or loss screen shall display the computed profit or loss relative to the initial deposit.

6. Data Integrity and Business Rules Enforcement
   6.1. Negative Balance Prevention:  
       - The system must enforce that a user cannot withdraw an amount that would cause a negative account balance.
   6.2. Overbuy Prevention:  
       - The system must enforce that a user cannot initiate a purchase of shares if the total purchase cost exceeds the available funds.
   6.3. Oversell Prevention:  
       - The system must enforce that a user cannot sell shares if the quantity specified exceeds the number of shares currently held.

7. Integration Details
   7.1. get_share_price(symbol) Function Integration:  
       - The system shall integrate with the provided function get_share_price(symbol) to retrieve current share prices.  
       - During testing, ensure that the function returns fixed prices for AAPL, TSLA, and GOOGL as expected.  
   7.2. Data Persistence and Storage:  
       - All user data, transactions, and portfolio holdings shall be persisted in a secure and reliable data store to support reporting and historical analysis.

8. User Interface Usability and Accessibility
   8.1. Navigation:  
       - The user interface should clearly allow navigation between the login, current share price, bond interest rates, transactions, portfolio, profit or loss, and holdings screens.
   8.2. Responsive Design:  
       - The UI should be designed responsively to work across different devices and screen sizes.
   8.3. Data Refresh:  
       - The UI screens displaying market data (share prices and bond interest rates) should support periodic updates or a refresh mechanism to ensure data is current.

This detailed list of requirements will serve as the basis for the engineering lead to design and implement the simple account management system for the trading simulation platform.