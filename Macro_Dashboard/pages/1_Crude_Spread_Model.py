import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Crude Spread Model", layout="wide")
st.title("🛢️ Brent-WTI Spread Model")

st.sidebar.markdown("---")
st.sidebar.markdown("**Built by Conner Butler**")
st.sidebar.markdown("Capital Markets Lab | 2026")

def get_spread_data(period: str = "2y") -> pd.DataFrame:
    raw = yf.download(["BZ=F", "CL=F"], period=period, auto_adjust=True)["Close"]
    raw.columns = ["Brent", "WTI"]
    raw = raw.dropna()
    raw["Spread"] = raw["Brent"] - raw["WTI"]
    raw["Structure"] = raw["Spread"].apply(lambda x: "Brent Premium" if x > 0 else "WTI Premium")
    raw["Spread_30d_Avg"] = raw["Spread"].rolling(30).mean()
    raw["Spread_Std"] = raw["Spread"].rolling(30).std()
    raw["Zscore"] = (raw["Spread"] - raw["Spread_30d_Avg"]) / raw["Spread_Std"]
    return raw

with st.spinner("Fetching live spread data..."):
    df = get_spread_data()

latest = df.iloc[-1]

# --- Live Metrics ---
st.subheader("Live Spread Metrics")
st.caption("Current Brent-WTI spread, 30-day average, and Z-score derived from live market prices.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Current Spread", f"$ {latest['Spread']:.2f}")
col2.metric("30D Avg Spread", f"$ {latest['Spread_30d_Avg']:.2f}")
col3.metric("Z-Score", f"{latest['Zscore']:.2f}")
col4.metric("Structure", latest["Structure"])

# Z-score signal warning
if abs(latest["Zscore"]) > 2:
    st.warning("⚠️ Z-Score beyond ±2 — spread is statistically stretched. Mean reversion likely.")

# --- Spread History ---
st.subheader("Spread History (Brent - WTI)")
st.caption("Daily Brent-WTI price differential over 2 years. "
           "Persistent positive values indicate Brent premium driven by geopolitical risk or supply constraints.")
st.line_chart(df["Spread"])

# --- Z-Score Chart ---
st.subheader("Rolling 30-Day Z-Score")
st.caption("Measures how far the current spread deviates from its 30-day mean in standard deviations. "
           "Values beyond ±2 signal potential mean reversion opportunities.")
st.line_chart(df["Zscore"])

# --- Brent vs WTI Prices ---
st.subheader("Brent vs WTI Price History")
st.caption("Raw price comparison between Brent and WTI crude. "
           "Divergences between the two drive spread expansion and compression.")
st.line_chart(df[["Brent", "WTI"]])

# --- Trade Signal ---
st.subheader("Spread Trade Signal")
st.caption("Signal generated from Z-score thresholds. "
           "A high Z-score favors shorting the spread; a low Z-score favors buying it.")

zscore = latest["Zscore"]
if zscore > 2:
    st.error("📉 SHORT the Spread — Brent historically expensive vs WTI. Expect compression.")
elif zscore < -2:
    st.success("📈 LONG the Spread — Brent historically cheap vs WTI. Expect expansion.")
else:
    st.info("⏳ NEUTRAL — Spread within normal range. No high-conviction signal.")

# --- Raw Data ---
st.subheader("Raw Spread Data")
st.caption("Full daily spread history. Export or inspect for further analysis.")
with st.expander("View Raw Data"):
    st.dataframe(df.tail(20), width='stretch')
