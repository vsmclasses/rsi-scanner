import pandas as pd
import numpy as np


# ==============================
# RSI (Wilder RSI)
# ==============================

def calculate_rsi(close, period=14):

    delta = close.diff()

    gain = delta.where(delta > 0, 0)

    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()

    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi


# ==============================
# SMA
# ==============================

def calculate_sma(close, period=7):

    return close.rolling(period).mean()
