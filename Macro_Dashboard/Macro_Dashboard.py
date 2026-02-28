import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
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

# --- Dynamic Market Signals ---
st.subheader("Live Market Signals (1-Month Trend)")
st.caption("Auto-generated signals based on current vs. 1-month-ago prices. "
           "Reflects real-time directional bias for each asset.")

latest = prices.iloc[-1]
one_month_ago = prices.index[-1] - pd.DateOffset(months=1)
prev = prices.loc[prices.index.asof(one_month_ago)]

col1, col2, col3, col4, col5 = st.columns(5)
cols = [col1, col2, col3, col4, col5]

for i, asset in enumerate(prices.columns):
    change = ((latest[asset] - prev[asset]) / prev[asset]) * 100
    direction = "↑" if change > 0 else "↓"
    cols[i].metric(asset, f"{direction} {abs(change):.1f}%",
                   delta=f"{change:.1f}% (1M)")

# --- Dynamic Trade Ideas ---
st.subheader("Trade Ideas")
st.caption("Forward-looking positions derived from current price trends, volatility regimes, "
           "and macro correlations shown above. Updated dynamically based on live data.")

# Volatility warning
wti_vol = vol["WTI Crude"].iloc[-1]
nat_gas_vol = vol["Nat Gas"].iloc[-1]

if wti_vol > 0.45 or nat_gas_vol > 0.80:
    st.warning("⚠️ High volatility detected — trade signals may be less reliable. "
               "Use additional confirmation before acting.")

wti_trend = "bullish" if latest["WTI Crude"] > prev["WTI Crude"] else "bearish"
brent_trend = "bullish" if latest["Brent Crude"] > prev["Brent Crude"] else "bearish"
gas_trend = "bullish" if latest["Nat Gas"] > prev["Nat Gas"] else "bearish"
usd_trend = "weakening" if latest["USD Index"] < prev["USD Index"] else "strengthening"
yield_trend = "rising" if latest["10Y Yield"] > prev["10Y Yield"] else "falling"

wti_direction = "📈 Long" if wti_trend == "bullish" else "📉 Short"
gas_direction = "📈 Long" if gas_trend == "bullish" else "📉 Short"
usd_direction = "📉 Short" if usd_trend == "weakening" else "📈 Long"
spread_direction = "📈 Long Spread" if brent_trend == "bullish" and wti_trend == "bearish" else "📉 Short Spread"

# USD-aware WTI and Brent thesis
wti_usd_context = (
    "USD weakness supports crude upside — oil cheaper for foreign buyers."
    if usd_trend == "weakening"
    else "Note: USD strength is a headwind for crude — monitor for price resistance."
)

brent_usd_context = (
    "USD weakness amplifies Brent upside for non-USD buyers."
    if usd_trend == "weakening"
    else "Note: USD strength may cap Brent gains despite geopolitical premium."
)

trade_ideas = pd.DataFrame([
    {
        "Asset": "WTI Crude (CL=F)",
        "Direction": wti_direction,
        "Thesis": f"1M trend is {wti_trend}. {wti_usd_context} {'Supply draw adds further support.' if wti_trend == 'bullish' else 'Watch for support breakdown.'}",
        "Risk": "Demand slowdown, China PMI miss"
    },
    {
        "Asset": "Nat Gas (NG=F)",
        "Direction": gas_direction,
        "Thesis": f"1M trend is {gas_trend}. Low correlation to crude means idiosyncratic move. {'Storage deficit entering summer.' if gas_trend == 'bullish' else 'Oversupply risk near-term.'}",
        "Risk": "Warm weather forecast, LNG export delays"
    },
    {
        "Asset": "USD Index (DX-Y.NYB)",
        "Direction": usd_direction,
        "Thesis": f"USD is {usd_trend} with 10Y yields {yield_trend}. {'Rate differential narrowing vs peers — bearish USD.' if usd_trend == 'weakening' else 'Rate support keeping USD bid near-term.'}",
        "Risk": "Fed hawkish surprise, risk-off flight to USD"
    },
    {
        "Asset": "Brent Crude (BZ=F)",
        "Direction": "📈 Long" if brent_trend == "bullish" else "📉 Short",
        "Thesis": f"1M trend is {brent_trend}. {brent_usd_context} {'Geopolitical premium building.' if brent_trend == 'bullish' else 'Demand concerns pressuring price.'}",
        "Risk": "US export surge, OPEC policy shift"
    },
])

st.dataframe(trade_ideas, use_container_width=True)
