import gradio as gr
import datetime
from accounts import Account, get_current_share_prices, get_bond_interest_rates, get_currency_rates, get_latest_news

# Global state to track logged-in user
current_user = None

# Theme colors
PRIMARY_COLOR = "#1f2937"
SECONDARY_COLOR = "#374151"
ACCENT_COLOR = "#3b82f6"
SUCCESS_COLOR = "#10b981"
WARNING_COLOR = "#f59e0b"
ERROR_COLOR = "#ef4444"
BACKGROUND_COLOR = "#f9fafb"

def login(email, password):
    global current_user
    try:
        current_user = Account.login(email, password)
        return f"✅ Logged in as {email}", gr.update(visible=False), gr.update(visible=True)
    except ValueError as e:
        return f"❌ Login failed: {str(e)}", gr.update(visible=True), gr.update(visible=False)

def register(email, password):
    try:
        Account.register(email, password)
        return f"✅ Registered successfully! Please login."
    except ValueError as e:
        return f"❌ Registration failed: {str(e)}"

def deposit(amount):
    if not current_user:
        return "❌ Please login first"
    try:
        current_user.deposit_funds(amount)
        return f"✅ Deposited ${amount:.2f}. New balance: ${current_user.funds:.2f}"
    except ValueError as e:
        return f"❌ Deposit failed: {str(e)}"

def withdraw(amount):
    if not current_user:
        return "❌ Please login first"
    try:
        current_user.withdraw_funds(amount)
        return f"✅ Withdrew ${amount:.2f}. New balance: ${current_user.funds:.2f}"
    except ValueError as e:
        return f"❌ Withdrawal failed: {str(e)}"

def buy_shares(symbol, quantity):
    if not current_user:
        return "❌ Please login first"
    try:
        current_user.buy_shares(symbol, quantity)
        return f"✅ Bought {quantity} shares of {symbol.upper()}"
    except ValueError as e:
        return f"❌ Buy failed: {str(e)}"

def sell_shares(symbol, quantity):
    if not current_user:
        return "❌ Please login first"
    try:
        current_user.sell_shares(symbol, quantity)
        return f"✅ Sold {quantity} shares of {symbol.upper()}"
    except ValueError as e:
        return f"❌ Sell failed: {str(e)}"

def get_portfolio_info():
    if not current_user:
        return "Please login to view portfolio"
    
    holdings = current_user.get_holdings_detail()
    if not holdings:
        holdings_text = "No holdings"
    else:
        holdings_text = "\n".join([f"{h['symbol']}: {h['quantity']} shares @ ${h['current_price']:.2f} = ${h['current_value']:.2f}" for h in holdings])
    
    return f"""
Cash: ${current_user.funds:.2f}
Holdings Value: ${current_user.get_holdings_value():.2f}
Total Portfolio Value: ${current_user.get_portfolio_value():.2f}
Profit/Loss: ${current_user.get_profit_loss():.2f}

Holdings:
{holdings_text}
"""

def get_transactions():
    if not current_user:
        return "Please login to view transactions"
    
    transactions = current_user.get_transaction_history()
    if not transactions:
        return "No transactions yet"
    
    result = []
    for t in transactions:
        time = datetime.datetime.fromisoformat(t['timestamp']).strftime("%Y-%m-%d %H:%M")
        if t['type'] == 'deposit':
            result.append(f"{time} - Deposit: ${t['amount']:.2f}")
        elif t['type'] == 'withdrawal':
            result.append(f"{time} - Withdrawal: ${t['amount']:.2f}")
        elif t['type'] == 'buy':
            result.append(f"{time} - Buy {t['quantity']} {t['symbol']} @ ${t['price']:.2f} = ${t['total_cost']:.2f}")
        elif t['type'] == 'sell':
            result.append(f"{time} - Sell {t['quantity']} {t['symbol']} @ ${t['price']:.2f} = ${t['total_value']:.2f}")
    
    return "\n".join(result)

def get_share_prices_display():
    prices = get_current_share_prices()
    return "\n".join([f"{symbol}: ${price:.2f}" for symbol, price in prices.items()])

def get_bond_rates_display():
    rates = get_bond_interest_rates()
    return "\n".join([f"{term}: {rate*100:.1f}%" for term, rate in rates.items()])

def get_currency_rates_display():
    rates = get_currency_rates()
    return "\n".join([f"{currency}: {rate:.2f}" for currency, rate in rates.items()])

def get_news_display():
    news = get_latest_news()
    return "\n\n".join([f"**{n['title']}**\n{n['summary']}" for n in news])

def exchange_currency(from_currency, to_currency, amount):
    rates = get_currency_rates()
    if from_currency not in rates or to_currency not in rates:
        return "Invalid currency"
    
    converted = amount * (rates[to_currency] / rates[from_currency])
    return f"{amount} {from_currency} = {converted:.2f} {to_currency}"

with gr.Blocks(theme=gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="slate",
    neutral_hue="gray"
)) as app:
    gr.Markdown("# 🏦 Trading Simulation Platform")
    
    with gr.Tab("Login / Register"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Login")
                email_input = gr.Textbox(label="Email", placeholder="user@example.com")
                password_input = gr.Textbox(label="Password", type="password", placeholder="password")
                login_btn = gr.Button("Login", variant="primary")
                login_output = gr.Textbox(label="Status", interactive=False)
                
            with gr.Column(scale=1):
                gr.Markdown("### Register")
                reg_email = gr.Textbox(label="Email", placeholder="user@example.com")
                reg_password = gr.Textbox(label="Password", type="password", placeholder="password")
                register_btn = gr.Button("Register", variant="secondary")
                reg_output = gr.Textbox(label="Status", interactive=False)
    
    with gr.Tab("Account Management"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Deposit Funds")
                deposit_amount = gr.Number(label="Amount", value=1000)
                deposit_btn = gr.Button("Deposit", variant="primary")
                deposit_output = gr.Textbox(label="Result", interactive=False)
                
            with gr.Column():
                gr.Markdown("### Withdraw Funds")
                withdraw_amount = gr.Number(label="Amount", value=100)
                withdraw_btn = gr.Button("Withdraw", variant="primary")
                withdraw_output = gr.Textbox(label="Result", interactive=False)
    
    with gr.Tab("Trading"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Buy Shares")
                buy_symbol = gr.Textbox(label="Symbol", placeholder="AAPL")
                buy_quantity = gr.Number(label="Quantity", value=10, minimum=1)
                buy_btn = gr.Button("Buy", variant="success")
                buy_output = gr.Textbox(label="Result", interactive=False)
                
            with gr.Column():
                gr.Markdown("### Sell Shares")
                sell_symbol = gr.Textbox(label="Symbol", placeholder="AAPL")
                sell_quantity = gr.Number(label="Quantity", value=10, minimum=1)
                sell_btn = gr.Button("Sell", variant="error")
                sell_output = gr.Textbox(label="Result", interactive=False)
    
    with gr.Tab("Portfolio"):
        portfolio_display = gr.Textbox(
            label="Portfolio Overview",
            lines=10,
            interactive=False,
            value="Please login to view your portfolio"
        )
        refresh_portfolio = gr.Button("Refresh")
    
    with gr.Tab("Transactions"):
        transactions_display = gr.Textbox(
            label="Transaction History",
            lines=15,
            interactive=False,
            value="Please login to view transactions"
        )
        refresh_transactions = gr.Button("Refresh")
    
    with gr.Tab("Market Data"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Current Share Prices")
                share_prices = gr.Textbox(
                    label="Prices",
                    lines=5,
                    interactive=False,
                    value=get_share_prices_display()
                )
                refresh_prices = gr.Button("Refresh Prices")
                
            with gr.Column():
                gr.Markdown("### Bond Interest Rates")
                bond_rates = gr.Textbox(
                    label="Rates",
                    lines=10,
                    interactive=False,
                    value=get_bond_rates_display()
                )
    
    with gr.Tab("Currency Exchange"):
        gr.Markdown("### Current Exchange Rates")
        currency_rates_display = gr.Textbox(
            label="Rates",
            lines=8,
            interactive=False,
            value=get_currency_rates_display()
        )
        
        gr.Markdown("### Exchange Calculator")
        with gr.Row():
            from_currency = gr.Dropdown(
                choices=list(get_currency_rates().keys()),
                label="From Currency",
                value="USD"
            )
            to_currency = gr.Dropdown(
                choices=list(get_currency_rates().keys()),
                label="To Currency",
                value="EUR"
            )
            amount = gr.Number(label="Amount", value=100)
        exchange_btn = gr.Button("Calculate", variant="primary")
        exchange_result = gr.Textbox(label="Result", interactive=False)
    
    with gr.Tab("News"):
        news_display = gr.Textbox(
            label="Latest News",
            lines=10,
            interactive=False,
            value=get_news_display()
        )
        refresh_news = gr.Button("Refresh News")
    
    # Event handlers
    login_btn.click(
        fn=login,
        inputs=[email_input, password_input],
        outputs=[login_output, gr.State(), gr.State()]
    )
    
    register_btn.click(
        fn=register,
        inputs=[reg_email, reg_password],
        outputs=[reg_output]
    )
    
    deposit_btn.click(
        fn=deposit,
        inputs=[deposit_amount],
        outputs=[deposit_output]
    )
    
    withdraw_btn.click(
        fn=withdraw,
        inputs=[withdraw_amount],
        outputs=[withdraw_output]
    )
    
    buy_btn.click(
        fn=buy_shares,
        inputs=[buy_symbol, buy_quantity],
        outputs=[buy_output]
    )
    
    sell_btn.click(
        fn=sell_shares,
        inputs=[sell_symbol, sell_quantity],
        outputs=[sell_output]
    )
    
    refresh_portfolio.click(
        fn=get_portfolio_info,
        outputs=[portfolio_display]
    )
    
    refresh_transactions.click(
        fn=get_transactions,
        outputs=[transactions_display]
    )
    
    refresh_prices.click(
        fn=get_share_prices_display,
        outputs=[share_prices]
    )
    
    exchange_btn.click(
        fn=exchange_currency,
        inputs=[from_currency, to_currency, amount],
        outputs=[exchange_result]
    )
    
    refresh_news.click(
        fn=get_news_display,
        outputs=[news_display]
    )

if __name__ == "__main__":
    app.launch()