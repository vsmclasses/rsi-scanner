import yfinance as yf
import pandas as pd

from indicators import calculate_rsi, calculate_sma


# ==========================
# Load Stock List
# ==========================

with open("symbols.txt") as f:
    symbols = [x.strip() for x in f if x.strip()]

print("Total Symbols :", len(symbols))


# ==========================
# Test One Stock
# ==========================

symbol = symbols[0]

print("Downloading :", symbol)

df = yf.download(
    symbol + ".NS",
    period="1y",
    interval="1d",
    progress=False,
    auto_adjust=False
)

print(df.tail())
