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

        df = yf.download(

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
