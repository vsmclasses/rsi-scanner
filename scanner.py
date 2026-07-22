import pandas as pd
import yfinance as yf

from indicators import calculate_rsi
from indicators import calculate_sma

from config import *


# --------------------------
# Load Symbols
# --------------------------

with open("symbols.txt") as f:
    SYMBOLS = [x.strip() for x in f if x.strip()]


print("Total Stocks :", len(SYMBOLS))


# --------------------------
# Download Function
# --------------------------

def download_stock(symbol):

    try:
from indicators import create_weekly
from indicators import create_monthly
        df = yf.download(


            df.index = pd.to_datetime(df.index)

daily = df.copy()

weekly = create_weekly(df)

monthly = create_monthly(df)
# =====================================
# Daily Indicators
# =====================================

daily["RSI"] = calculate_rsi(daily["Close"], 14)

daily["SMA7"] = calculate_sma(daily["Close"], 7)

# =====================================
# Weekly Indicators
# =====================================

weekly["RSI"] = calculate_rsi(weekly["Close"], 14)

# =====================================
# Monthly Indicators
# =====================================

monthly["RSI"] = calculate_rsi(monthly["Close"], 14)

last = daily.iloc[-1]

prev = daily.iloc[-2]

weekly_last = weekly.iloc[-1]

monthly_last = monthly.iloc[-1]

print()

print("----------------------")

print("Current Price :", round(last["Close"],2))

print("Previous RSI :", round(prev["RSI"],2))

print("Current RSI :", round(last["RSI"],2))

print("Weekly RSI :", round(weekly_last["RSI"],2))

print("Monthly RSI :", round(monthly_last["RSI"],2))

print("SMA 7 :", round(last["SMA7"],2))

print(daily.tail())

print(weekly.tail())

print(monthly.tail())
            symbol + ".NS",

            period=DOWNLOAD_PERIOD,

            interval=DOWNLOAD_INTERVAL,

            auto_adjust=False,

            progress=False

        )

        if len(df) == 0:

            return None

        return df

    except:

        return None

# --------------------------
# Test Download
# --------------------------

df = download_stock(SYMBOLS[0])

print(df.tail())
