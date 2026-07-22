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
