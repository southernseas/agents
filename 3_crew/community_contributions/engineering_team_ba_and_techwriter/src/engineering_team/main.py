#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from engineering_team.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

requirements = """
A simple account management system for a trading simulation platform.
The system should allow users to create an account, deposit funds, and withdraw funds.
The system should allow users to record that they have bought or sold shares, providing a quantity.
The system should calculate the total value of the user's portfolio, and the profit or loss from the initial deposit.
The system should be able to report the holdings of the user at any point in time.
The system should be able to report the profit or loss of the user at any point in time.
The system should be able to list the transactions that the user has made over time.
The system should prevent the user from withdrawing funds that would leave them with a negative balance, or
 from buying more shares than they can afford, or selling shares that they don't have.
 The system has access to a function get_share_price(symbol) which returns the current price of a share, and includes a test implementation that returns fixed prices for AAPL, TSLA, GOOGL.
 The system should have a user login screen that allows the user to login to the system.
 The system should have a 'current share price' screen that displays the current share price of the shares,
 The systen should have a 'bond interest rates' screen that displays the current bond interest rates of the bonds : 1-month, 3-month, 6-month, 1-year, 2-year, 3-year, 5-year, 10-year, 20-year, 30-year.
 The system should have a 'transactions' screen that displays the transactions that the user has made over time.
 The system should have a 'portfolio' screen that displays the holdings of the user at any point in time.
 The system should have a 'profit or loss' screen that displays the profit or loss of the user at any point in time.
 The system should have a 'holdings' screen that displays the holdings of the user at any point in time.
 The system should have a 'transactions' screen that displays the transactions that the user has made over time.
 The system should have a 'portfolio' screen that displays the holdings of the user at any point in time.
 the system shiuld have a 'currency exchange' screen that allows the user to exchange currency.
 the system should have a 'news' screen that displays the latest news.
 the system should have a "currency rates" screen that displays the current currency rates.
"""
module_name = "accounts.py"
class_name = "Account"


def run():
    """
    Run the research crew.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name
    }

    # Create and run the crew
    result = EngineeringTeam().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()