import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from analysis import get_prices, compute_returns, compute_rolling_vol, compute_correlation

st.set_page_config(page_title="Macro & Commodities Dashboard", layout="wide")
st.title("🛢️ Global Macro & Commodities Dashboard")

TICKERS = ["CL=F", "BZ=F", "NG=F", "^TNX", "DX-Y.NYB"]
NAMES = {"CL=F": "WTI Crude", "BZ=F": "Brent Crude", "NG=F": "Nat Gas",
         "^TNX": "10Y Yield", "DX-Y.NYB": "USD Index"}

with st.spinner("Fetching live data..."):
    prices = get_prices(TICKERS, period="2y")
    prices.columns = [NAMES[t] for t in prices.columns]

# --- Price Chart ---
st.subheader("Price History")
st.line_chart(prices)

# --- Rolling Volatility ---
st.subheader("30-Day Rolling Volatility (Annualized)")
vol = compute_rolling_vol(prices)
st.line_chart(vol)

# --- Correlation Heatmap ---
st.subheader("Correlation Matrix")
corr = compute_correlation(prices)
fig, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
st.pyplot(fig)

# --- Raw Data ---
with st.expander("View Raw Price Data"):
    st.dataframe(prices.tail(20))
