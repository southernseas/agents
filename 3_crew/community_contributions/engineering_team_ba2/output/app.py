import gradio as gr
import pandas as pd
from typing import Dict, List
from accounts import Account, get_share_price

# Global storage for logged-in account
current_account = None

# Bond rates
BOND_RATES = {
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

# Stock symbols
STOCK_SYMBOLS = ['AAPL', 'TSLA', 'GOOGL']

def create_account(username: str, email: str, password: str) -> str:
    """Create a new account."""
    global current_account
    try:
        current_account = Account(username, email, password)
        return f"Account created successfully for {username}"
    except ValueError as e:
        return str(e)

def login(password: str) -> str:
    """Login to existing account."""
    global current_account
    if current_account is None:
        return "No account exists. Please create an account first."
    if current_account.login(password):
        return f"Logged in as {current_account.username}"
    return "Invalid password"

def deposit(amount: float) -> str:
    """Deposit funds."""
    global current_account
    if current_account is None:
        return "No account exists"
    try:
        current_account.deposit_funds(amount)
        return f"Deposited ${amount:.2f}. New balance: ${current_account.balance:.2f}"
    except ValueError as e:
        return str(e)

def withdraw(amount: float) -> str:
    """Withdraw funds."""
    global current_account
    if current_account is None:
        return "No account exists"
    try:
        if current_account.withdraw_funds(amount):
            return f"Withdrew ${amount:.2f}. New balance: ${current_account.balance:.2f}"
        return "Insufficient funds"
    except ValueError as e:
        return str(e)

def buy_shares(symbol: str, quantity: int) -> str:
    """Buy shares."""
    global current_account
    if current_account is None:
        return "No account exists"
    try:
        if current_account.buy_shares(symbol, quantity):
            price = get_share_price(symbol)
            total = price * quantity
            return f"Bought {quantity} shares of {symbol} at ${price:.2f}/share for ${total:.2f}"
        return "Insufficient funds"
    except ValueError as e:
        return str(e)

def sell_shares(symbol: str, quantity: int) -> str:
    """Sell shares."""
    global current_account
    if current_account is None:
        return "No account exists"
    try:
        if current_account.sell_shares(symbol, quantity):
            price = get_share_price(symbol)
            total = price * quantity
            return f"Sold {quantity} shares of {symbol} at ${price:.2f}/share for ${total:.2f}"
        return "Insufficient shares"
    except ValueError as e:
        return str(e)

def get_holdings() -> pd.DataFrame:
    """Get current holdings."""
    global current_account
    if current_account is None:
        return pd.DataFrame()
    
    holdings = current_account.get_holdings_report()
    if not holdings:
        return pd.DataFrame(columns=['Symbol', 'Quantity', 'Current Price', 'Total Value'])
    
    data = []
    for symbol, info in holdings.items():
        data.append({
            'Symbol': symbol,
            'Quantity': info['quantity'],
            'Current Price': f"${info['current_price']:.2f}",
            'Total Value': f"${info['total_value']:.2f}"
        })
    return pd.DataFrame(data)

def get_transactions() -> pd.DataFrame:
    """Get transaction history."""
    global current_account
    if current_account is None:
        return pd.DataFrame()
    
    transactions = current_account.get_transactions()
    if not transactions:
        return pd.DataFrame(columns=['Date', 'Type', 'Symbol', 'Quantity', 'Amount', 'Balance'])
    
    data = []
    for t in transactions:
        data.append({
            'Date': t['datetime'][:19],
            'Type': t['type'],
            'Symbol': t['symbol'] or '',
            'Quantity': t['quantity'] or '',
            'Amount': f"${t['amount']:.2f}",
            'Balance': f"${t['balance']:.2f}"
        })
    return pd.DataFrame(data)

def get_portfolio_summary() -> Dict:
    """Get portfolio summary."""
    global current_account
    if current_account is None:
        return {"Error": "No account exists"}
    
    summary = current_account.get_portfolio_summary()
    pnl = current_account.compute_profit_or_loss()
    
    return {
        'Portfolio Value': f"${summary['portfolio_value']:.2f}",
        'Available Balance': f"${summary['available_balance']:.2f}",
        'Total Profit/Loss': f"${pnl:.2f}",
        'Total Value': f"${summary['portfolio_value'] + summary['available_balance']:.2f}"
    }

def get_share_prices() -> pd.DataFrame:
    """Get current share prices."""
    prices = {s: get_share_price(s) for s in STOCK_SYMBOLS}
    return pd.DataFrame(list(prices.items()), columns=['Symbol', 'Price'])

def get_bond_rates() -> pd.DataFrame:
    """Get bond interest rates."""
    return pd.DataFrame(list(BOND_RATES.items()), columns=['Maturity', 'Rate (%)'])

# Create Gradio interface
with gr.Blocks(title="Trading Simulation Platform") as demo:
    gr.Markdown("# Trading Simulation Platform")
    
    with gr.Tab("Account Management"):
        gr.Markdown("## Create Account")
        with gr.Row():
            username = gr.Textbox(label="Username")
            email = gr.Textbox(label="Email")
            password = gr.Textbox(label="Password", type="password")
        create_btn = gr.Button("Create Account")
        create_output = gr.Textbox(label="Result")
        
        gr.Markdown("## Login")
        login_password = gr.Textbox(label="Password", type="password")
        login_btn = gr.Button("Login")
        login_output = gr.Textbox(label="Login Result")
        
    with gr.Tab("Funds"):
        gr.Markdown("## Deposit/Withdraw Funds")
        with gr.Row():
            deposit_amount = gr.Number(label="Deposit Amount", value=0)
            deposit_btn = gr.Button("Deposit")
            deposit_output = gr.Textbox(label="Deposit Result")
            
        with gr.Row():
            withdraw_amount = gr.Number(label="Withdraw Amount", value=0)
            withdraw_btn = gr.Button("Withdraw")
            withdraw_output = gr.Textbox(label="Withdraw Result")
            
    with gr.Tab("Trading"):
        gr.Markdown("## Buy/Sell Shares")
        with gr.Row():
            buy_symbol = gr.Dropdown(choices=STOCK_SYMBOLS, label="Symbol")
            buy_quantity = gr.Number(label="Quantity", value=1, minimum=1)
            buy_btn = gr.Button("Buy")
            buy_output = gr.Textbox(label="Buy Result")
            
        with gr.Row():
            sell_symbol = gr.Dropdown(choices=STOCK_SYMBOLS, label="Symbol")
            sell_quantity = gr.Number(label="Quantity", value=1, minimum=1)
            sell_btn = gr.Button("Sell")
            sell_output = gr.Textbox(label="Sell Result")
            
    with gr.Tab("Portfolio"):
        gr.Markdown("## Portfolio Summary")
        portfolio_summary = gr.JSON(label="Summary")
        refresh_portfolio = gr.Button("Refresh")
        
        gr.Markdown("## Current Holdings")
        holdings_table = gr.Dataframe(headers=["Symbol", "Quantity", "Current Price", "Total Value"])
        refresh_holdings = gr.Button("Refresh Holdings")
        
    with gr.Tab("Transactions"):
        gr.Markdown("## Transaction History")
        transactions_table = gr.Dataframe(headers=["Date", "Type", "Symbol", "Quantity", "Amount", "Balance"])
        refresh_transactions = gr.Button("Refresh Transactions")
        
    with gr.Tab("Market Data"):
        gr.Markdown("## Current Share Prices")
        prices_table = gr.Dataframe(headers=["Symbol", "Price"])
        refresh_prices = gr.Button("Refresh Prices")
        
        gr.Markdown("## Bond Interest Rates")
        rates_table = gr.Dataframe(headers=["Maturity", "Rate (%)"])
        refresh_rates = gr.Button("Refresh Rates")
    
    # Event handlers
    create_btn.click(create_account, [username, email, password], create_output)
    login_btn.click(login, login_password, login_output)
    
    deposit_btn.click(deposit, deposit_amount, deposit_output)
    withdraw_btn.click(withdraw, withdraw_amount, withdraw_output)
    
    buy_btn.click(buy_shares, [buy_symbol, buy_quantity], buy_output)
    sell_btn.click(sell_shares, [sell_symbol, sell_quantity], sell_output)
    
    refresh_portfolio.click(get_portfolio_summary, None, portfolio_summary)
    refresh_holdings.click(get_holdings, None, holdings_table)
    refresh_transactions.click(get_transactions, None, transactions_table)
    refresh_prices.click(get_share_prices, None, prices_table)
    refresh_rates.click(get_bond_rates, None, rates_table)
    
    # Auto-refresh on tab change
    def load_data():
        return get_portfolio_summary(), get_holdings(), get_transactions(), get_share_prices(), get_bond_rates()
    
    demo.load(load_data, None, [portfolio_summary, holdings_table, transactions_table, prices_table, rates_table])

if __name__ == "__main__":
    demo.launch()