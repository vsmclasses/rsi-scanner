import pandas as pd


# ==========================================================
# RSI (Wilder)
# ==========================================================

def calculate_rsi(close, period=14):

    delta = close.diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/period,
                        adjust=False,
                        min_periods=period).mean()

    avg_loss = loss.ewm(alpha=1/period,
                        adjust=False,
                        min_periods=period).mean()

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


# ==========================================================
# SMA
# ==========================================================

def calculate_sma(close, period=7):

    return close.rolling(period).mean()


# ==========================================================
# Weekly Candle
# ==========================================================

def create_weekly(df):

    weekly = pd.DataFrame()

    weekly["Open"] = df["Open"].resample("W-FRI").first()

    weekly["High"] = df["High"].resample("W-FRI").max()

    weekly["Low"] = df["Low"].resample("W-FRI").min()

    weekly["Close"] = df["Close"].resample("W-FRI").last()

    weekly["Volume"] = df["Volume"].resample("W-FRI").sum()

    return weekly.dropna()


# ==========================================================
# Monthly Candle
# ==========================================================

def create_monthly(df):

    monthly = pd.DataFrame()

    monthly["Open"] = df["Open"].resample("ME").first()

    monthly["High"] = df["High"].resample("ME").max()

    monthly["Low"] = df["Low"].resample("ME").min()

    monthly["Close"] = df["Close"].resample("ME").last()

    monthly["Volume"] = df["Volume"].resample("ME").sum()

    return monthly.dropna()
