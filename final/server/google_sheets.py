from mcp.server.fastmcp import FastMCP
from utils.startlette import create_starlette_app
import gspread
from gspread_dataframe import get_as_dataframe
import pandas as pd
from enum import Enum
from datetime import datetime
import os
from dotenv import load_dotenv
# load_dotenv("/Users/haripat/Desktop/SF/mcp_demo/.env")
load_dotenv("../../.env")


scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

gc = gspread.oauth(credentials_filename=os.getenv("GOOGLE_CREDENTIALS_FILE"), authorized_user_filename="authorized_user.json")
sheet = gc.open_by_key(os.getenv("GOOGLE_SHEETS_ID"))
worksheet = sheet.worksheet("Transactions")
df = get_as_dataframe(worksheet)

class Category(Enum):
    ALCOHOL = "Alcohol & Bars"
    AUTO_INSURANCE = "Auto Insurance"
    COFFEE_SHOPS = "Coffee Shops"
    CREDIT_CARD_PAYMENT = "Credit Card Payment"
    ELECTRONICS_SOFTWARE = "Electronics & Software"
    ENTERTAINMENT = "Entertainment"
    FAST_FOOD = "Fast Food"
    FOOD_DINING = "Food & Dining"
    GAS_FUEL = "Gas & Fuel"
    GROCERIES = "Groceries"
    HAIRCUT = "Haircut"
    HOME_IMPROVEMENT = "Home Improvement"
    INTERNET = "Internet"
    MOBILE_PHONE = "Mobile Phone"
    MORTGAGE_RENT = "Mortgage & Rent"
    MOVIES_DVD = "Movies & DVDs"
    MUSIC = "Music"
    PAYCHECK = "Paycheck"
    RESTAURANTS = "Restaurants"
    SHOPPING = "Shopping"
    TELEVISION = "Television"
    UTILITIES = "Utilities"

mcp = FastMCP("finance-sheets-server")

@mcp.tool()
def sample_transactions(number_of_sample: int) -> str:
    """
    Returns a sample of transactions from the user's personal finance transactions
    
    Args:
        number_of_sample: The number of transactions to sample
    """
    sampled_df = df.sample(number_of_sample)
    return sampled_df.to_string()

@mcp.tool()
def add_transaction(description: str, amount: float, category: Category) -> str:
    """
    Adds a transaction to the user's personal finance transactions
    
    Args:
        description: The description of the transaction
        amount: The amount of the transaction
        category: The category of the transaction
    """
    now = datetime.now()
    date_str = f"{now.month}/{now.day}/{now.strftime('%y')}"
    print(f"Adding transaction: {date_str}, {description}, {amount}, {category.value}")
    worksheet.append_row([date_str, description, amount, category.value])
    return "Transaction added successfully"

if __name__ == "__main__":
    mcp_server = mcp._mcp_server
    import uvicorn
    starlette_app = create_starlette_app(mcp_server, debug=True)
    uvicorn.run(starlette_app, host="localhost", port=8010)