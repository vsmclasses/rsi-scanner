import pandas as pd
import yfinance as yf

from indicators import *
from conditions import *
from sheets import *

# ---------------------------------------
# Load Stock List
# ---------------------------------------

with open("symbols.txt", "r") as f:
    SYMBOLS = [x.strip() for x in f.readlines() if x.strip()]

print(f"Total Stocks : {len(SYMBOLS)}")
