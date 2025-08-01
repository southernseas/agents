import gradio as gr
import datetime
from accounts import Account, get_share_price, get_current_share_prices, get_bond_interest_rates, get_currency_rates, get_latest_news

# Global variable to store the currently logged-in account
current_account = None

def login(username_or_email, password):
    global current_account
    account = Account.login(username_or_email, password)
    if account:
        current_account = account
        return f"Welcome, {account.username}! Login successful."
    return "Login failed. Please check your credentials."

def register(username, email, password):
    try:
        success = Account.register(username, email, password)
        if success:
            return f"Registration successful for {username}! You can now log in."
    except ValueError as e:
        return str(e)

def deposit(amount):
    global current_account
    if not current_account:
        return "Please login first"
    try:
        current_account.deposit_funds(float(amount))
        return f"Deposited ${amount:.2f}. New balance: ${current_account.balance:.2f}"
    except ValueError as e:
        return str(e)

def withdraw(amount):
    global current_account
    if not current_account:
        return "Please login first"
    try:
        current_account.withdraw_funds(float(amount))
        return f"Withdrew ${amount:.2f}. New balance: ${current_account.balance:.2f}"
    except ValueError as e:
        return str(e)

def buy_stock(symbol, quantity):
    global current_account
    if not current_account:
        return "Please login first"
    try:
        current_account.buy_stock(symbol, int(quantity))
        return f"Bought {quantity} shares of {symbol.upper()}"
    except ValueError as e:
        return str(e)

def sell_stock(symbol, quantity):
    global current_account
    if not current_account:
        return "Please login first"
    try:
        current_account.sell_stock(symbol, int(quantity))
        return f"Sold {quantity} shares of {symbol.upper()}"
    except ValueError as e:
        return str(e)

def get_portfolio():
    global current_account
    if not current_account:
        return "Please login first"
    
    portfolio_value = current_account.calculate_portfolio_value()
    profit_loss = current_account.calculate_profit_loss()
    holdings = current_account.get_holdings()
    
    holdings_str = "\n".join([f"{k}: {v} shares" for k, v in holdings.items()]) if holdings else "No holdings"
    
    return f"""
Portfolio Value: ${portfolio_value:.2f}
Profit/Loss: ${profit_loss:.2f}
Cash Balance: ${current_account.balance:.2f}
Holdings:
{holdings_str}
"""

def get_transactions():
    global current_account
    if not current_account:
        return "Please login first"
    
    transactions = current_account.get_transaction_history()
    if not transactions:
        return "No transactions yet"
    
    return "\n".join([str(t) for t in transactions])

def exchange_currency(from_currency, to_currency, amount):
    rates = get_currency_rates()
    if from_currency not in rates or to_currency not in rates:
        return "Invalid currency"
    
    try:
        amount = float(amount)
        converted = (amount / rates[from_currency]) * rates[to_currency]
        return f"{amount} {from_currency} = {converted:.2f} {to_currency}"
    except ValueError:
        return "Invalid amount"

with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue", secondary_hue="green", neutral_hue="slate")) as app:
    gr.Markdown("# 🏦 Trading Simulation Platform")
    
    with gr.Tab("🔐 Login/Register"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Login")
                username_login = gr.Textbox(label="Username or Email")
                password_login = gr.Textbox(label="Password", type="password")
                login_btn = gr.Button("Login", variant="primary")
                login_output = gr.Textbox(label="Login Status")
                
            with gr.Column():
                gr.Markdown("### Register")
                username_reg = gr.Textbox(label="Username")
                email_reg = gr.Textbox(label="Email")
                password_reg = gr.Textbox(label="Password", type="password")
                register_btn = gr.Button("Register", variant="secondary")
                register_output = gr.Textbox(label="Registration Status")
        
        login_btn.click(login, [username_login, password_login], login_output)
        register_btn.click(register, [username_reg, email_reg, password_reg], register_output)
    
    with gr.Tab("💰 Account Management"):
        gr.Markdown("### Manage Your Account")
        with gr.Row():
            deposit_amount = gr.Number(label="Deposit Amount", value=0)
            deposit_btn = gr.Button("Deposit", variant="primary")
        with gr.Row():
            withdraw_amount = gr.Number(label="Withdraw Amount", value=0)
            withdraw_btn = gr.Button("Withdraw", variant="secondary")
        account_output = gr.Textbox(label="Account Status")
        
        deposit_btn.click(deposit, deposit_amount, account_output)
        withdraw_btn.click(withdraw, withdraw_amount, account_output)
    
    with gr.Tab("📈 Stock Trading"):
        gr.Markdown("### Trade Stocks")
        with gr.Row():
            symbol_buy = gr.Textbox(label="Symbol to Buy", placeholder="AAPL, TSLA, GOOGL")
            quantity_buy = gr.Number(label="Quantity to Buy", value=1)
            buy_btn = gr.Button("Buy", variant="primary")
        
        with gr.Row():
            symbol_sell = gr.Textbox(label="Symbol to Sell", placeholder="AAPL, TSLA, GOOGL")
            quantity_sell = gr.Number(label="Quantity to Sell", value=1)
            sell_btn = gr.Button("Sell", variant="secondary")
        
        trade_output = gr.Textbox(label="Trade Status")
        
        buy_btn.click(buy_stock, [symbol_buy, quantity_buy], trade_output)
        sell_btn.click(sell_stock, [symbol_sell, quantity_sell], trade_output)
    
    with gr.Tab("📊 Current Share Prices"):
        gr.Markdown("### Live Stock Prices")
        prices_text = gr.Textbox(
            value="\n".join([f"{k}: ${v:.2f}" for k, v in get_current_share_prices().items()]),
            label="Current Prices",
            interactive=False
        )
    
    with gr.Tab("🏛️ Bond Interest Rates"):
        gr.Markdown("### Current Bond Rates")
        bonds_text = gr.Textbox(
            value="\n".join([f"{k}: {v*100:.2f}%" for k, v in get_bond_interest_rates().items()]),
            label="Bond Rates",
            interactive=False
        )
    
    with gr.Tab("💱 Currency Exchange"):
        gr.Markdown("### Exchange Currency")
        with gr.Row():
            from_currency = gr.Dropdown(
                choices=list(get_currency_rates().keys()),
                value="USD",
                label="From Currency"
            )
            to_currency = gr.Dropdown(
                choices=list(get_currency_rates().keys()),
                value="EUR",
                label="To Currency"
            )
        exchange_amount = gr.Number(label="Amount", value=100)
        exchange_btn = gr.Button("Exchange", variant="primary")
        exchange_output = gr.Textbox(label="Exchange Result")
        
        exchange_btn.click(exchange_currency, [from_currency, to_currency, exchange_amount], exchange_output)
    
    with gr.Tab("💼 Portfolio"):
        gr.Markdown("### Your Portfolio Overview")
        portfolio_btn = gr.Button("Refresh Portfolio", variant="primary")
        portfolio_output = gr.Textbox(label="Portfolio Details", lines=10)
        
        portfolio_btn.click(get_portfolio, [], portfolio_output)
    
    with gr.Tab("📜 Transactions"):
        gr.Markdown("### Transaction History")
        transactions_btn = gr.Button("Refresh Transactions", variant="primary")
        transactions_output = gr.Textbox(label="All Transactions", lines=15)
        
        transactions_btn.click(get_transactions, [], transactions_output)
    
    with gr.Tab("📰 News"):
        gr.Markdown("### Latest Financial News")
        news_text = gr.Textbox(
            value="\n".join([f"• {news}" for news in get_latest_news()]),
            label="News Headlines",
            interactive=False,
            lines=10
        )
    
    with gr.Tab("💵 Currency Rates"):
        gr.Markdown("### Current Currency Rates")
        currency_text = gr.Textbox(
            value="\n".join([f"{k}: {v}" for k, v in get_currency_rates().items()]),
            label="Exchange Rates (USD base)",
            interactive=False
        )

if __name__ == "__main__":
    app.launch()