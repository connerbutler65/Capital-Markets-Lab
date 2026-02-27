import yfinance as yf
import pandas as pd

def get_prices(tickers: list, period: str = "2y") -> pd.DataFrame:
    data = yf.download(tickers, period=period, auto_adjust=True)["Close"]
    return data

def compute_returns(df: pd.DataFrame) -> pd.DataFrame:
    return df.pct_change(fill_method=None).dropna()

def compute_rolling_vol(df: pd.DataFrame, window: int = 30) -> pd.DataFrame:
    returns = compute_returns(df)
    return returns.rolling(window).std() * (252 ** 0.5)  # annualized

def compute_correlation(df: pd.DataFrame) -> pd.DataFrame:
    return compute_returns(df).corr()
if __name__ == "__main__":
    tickers = ["CL=F", "BZ=F", "NG=F", "^TNX", "DX-Y.NYB"]
    prices = get_prices(tickers)
    print(prices.tail())
    print("\nCorrelation Matrix:")
    print(compute_correlation(prices))

print("--- Recent Prices ---")
print(prices.tail())
print("\n--- Correlation Matrix ---")
print(compute_correlation(prices))
