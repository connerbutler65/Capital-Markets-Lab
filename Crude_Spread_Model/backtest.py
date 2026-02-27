import pandas as pd
from spread_analysis import get_full_analysis


def run_backtest(df: pd.DataFrame, entry: float = 1.5) -> pd.DataFrame:
    df = df.copy().dropna()

    # Pure Z-score mean reversion signal
    df["Signal"] = 0
    df.loc[df["Zscore"] >  entry, "Signal"] = -1  # short spread when too wide
    df.loc[df["Zscore"] < -entry, "Signal"] =  1  # long spread when too tight

    df["Spread_Change"]   = df["Spread"].diff()
    df["Strategy_Return"] = -df["Signal"].shift(1) * df["Spread_Change"]
    df["Cumulative_PnL"]  = df["Strategy_Return"].cumsum()

    return df


def run_momentum_backtest(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().dropna()

    # Go long spread when above 30d avg, short when below
    df["Signal"] = 0
    df.loc[df["Spread"] > df["Spread_30d_Avg"], "Signal"] =  1
    df.loc[df["Spread"] < df["Spread_30d_Avg"], "Signal"] = -1

    df["Spread_Change"]   = df["Spread"].diff()
    df["Strategy_Return"] = df["Signal"].shift(1) * df["Spread_Change"]
    df["Cumulative_PnL"]  = df["Strategy_Return"].cumsum()

    return df


def print_stats(df: pd.DataFrame):
    trades    = df[df["Signal"] != 0]
    total_pnl = round(df["Cumulative_PnL"].iloc[-1], 2)
    win_days  = (df["Strategy_Return"] > 0).sum()
    loss_days = (df["Strategy_Return"] < 0).sum()
    total     = win_days + loss_days
    win_rate     = round(win_days / total * 100, 1) if total > 0 else 0
    max_drawdown = round((df["Cumulative_PnL"] - df["Cumulative_PnL"].cummax()).min(), 2)

    print(f"Total P&L:     ${total_pnl}")
    print(f"Win Rate:       {win_rate}%")
    print(f"Max Drawdown:  ${max_drawdown}")
    print(f"Total Signals:  {len(trades)}")


if __name__ == "__main__":
    df = get_full_analysis()

    print("--- Mean Reversion Strategy ---")
    results = run_backtest(df)
    print(results[["Spread", "Zscore", "Signal", "Cumulative_PnL"]].tail(10))
    print()
    print_stats(results)

    print("\n--- Momentum Strategy ---")
    momentum = run_momentum_backtest(df)
    print_stats(momentum)
