import yfinance as yf
import pandas as pd


def get_wti_curve(period: str = "2y") -> pd.DataFrame:
    raw = yf.download(["CL=F", "BZ=F"], period=period, auto_adjust=True)["Close"]
    raw.columns = ["Brent", "WTI"]
    return raw.dropna()


def compute_spread(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Spread"] = df["Brent"] - df["WTI"]
    return df


def classify_structure(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Structure"] = df["Spread"].apply(
        lambda x: "Brent Premium" if x > 0 else "WTI Premium"
    )
    return df


def compute_rolling_stats(df: pd.DataFrame, window: int = 30) -> pd.DataFrame:
    df = df.copy()
    df["Spread_30d_Avg"] = df["Spread"].rolling(window).mean()
    df["Spread_Std"]     = df["Spread"].rolling(window).std()
    df["Zscore"]         = (df["Spread"] - df["Spread_30d_Avg"]) / df["Spread_Std"]
    return df


def get_full_analysis(period: str = "2y") -> pd.DataFrame:
    df = get_wti_curve(period)
    df = compute_spread(df)
    df = classify_structure(df)
    df = compute_rolling_stats(df)
    return df


if __name__ == "__main__":
    df = get_full_analysis()
    print(df.tail(10))
    print("\nCurrent Structure:", df["Structure"].iloc[-1])
    print("Current Spread:   $", round(df["Spread"].iloc[-1], 2))
    print("Current Z-Score:  ", round(df["Zscore"].iloc[-1], 2))

