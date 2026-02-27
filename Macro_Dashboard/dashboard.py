import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from analysis import get_prices, compute_returns, compute_rolling_vol, compute_correlation

st.set_page_config(page_title="Macro & Commodities Dashboard", layout="wide")
st.title("🛢️ Global Macro & Commodities Dashboard")

st.sidebar.markdown("---")
st.sidebar.markdown("**Built by Conner Butler**")
st.sidebar.markdown("Capital Markets Lab | 2026")

TICKERS = ["CL=F", "BZ=F", "NG=F", "^TNX", "DX-Y.NYB"]
NAMES = {"CL=F": "WTI Crude", "BZ=F": "Brent Crude", "NG=F": "Nat Gas",
         "^TNX": "10Y Yield", "DX-Y.NYB": "USD Index"}

with st.spinner("Fetching live data..."):
    prices = get_prices(TICKERS, period="2y")
    prices.columns = [NAMES[t] for t in prices.columns]

# --- Price Chart ---
st.subheader("Price History")
st.caption("Tracks 2 years of daily closing prices across energy and macro assets. "
           "Used to identify regime shifts, trend direction, and relative performance.")
st.line_chart(prices)

# --- Rolling Volatility ---
st.subheader("30-Day Rolling Volatility (Annualized)")
st.caption("Measures how much each asset's price is fluctuating over the past 30 days, "
           "annualized. Spikes signal market stress or major supply/demand events.")
vol = compute_rolling_vol(prices)
st.line_chart(vol)

# --- Correlation Heatmap ---
st.subheader("Correlation Matrix")
st.caption("Shows how closely each pair of assets moves together. Values near +1 = move "
           "in sync, near -1 = move opposite, near 0 = no relationship. Key insight: "
           "Nat Gas is nearly uncorrelated with crude — it trades on its own fundamentals.")
corr = compute_correlation(prices)
fig, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
st.pyplot(fig)

# --- Raw Data ---
st.subheader("Raw Price Data")
st.caption("Full daily price history for all tracked assets. "
           "Export or inspect for further analysis.")
with st.expander("View Raw Price Data"):
    st.dataframe(prices.tail(20))
