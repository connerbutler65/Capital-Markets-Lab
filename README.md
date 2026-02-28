## Capital Markets Lab

A collection of Python-based financial analysis projects focused on commodities trading and macro research.

---

## Project 1: Macro & Commodities Dashboard

An interactive dashboard tracking global macro indicators and energy markets.

**Assets tracked:** WTI Crude, Brent Crude, Natural Gas, 10Y Treasury Yield, USD Index

**Features:**
- Live price history via Yahoo Finance
- 30-day rolling annualized volatility
- Cross-asset correlation heatmap
- Built with Python, Pandas, Streamlit, Seaborn

**Data Source:** Yahoo Finance (yfinance)

---

## Project 2: Crude Oil Spread Model & Backtest

A quantitative research tool analyzing the Brent-WTI crude oil spread using statistical signals and systematic trading strategies.

**Assets tracked:** Brent Crude (BZ=F), WTI Crude (CL=F)

**Features:**
- Live Brent-WTI spread calculation and classification
- 30-day rolling Z-score to identify statistically extreme spread levels
- Backtested mean reversion strategy (Z-score signal)
- Backtested momentum strategy (moving average crossover)
- Comparative strategy analysis across 2 years of data

**Key Finding:** Neither mean reversion (-$14.25 P&L) nor momentum (-$14.99 P&L) generated positive returns on the Brent-WTI spread over 2024–2026. The spread appears driven by structural supply factors rather than statistical price patterns. Future work: incorporate EIA crude inventory data as a fundamental signal layer.

**Current Signal (Feb 27 2026):** Spread $5.88 | Z-Score +2.22σ (Brent Premium)

**Data Source:** Yahoo Finance (yfinance)

---

## Setup

```bash
pip install -r requirements.txt
cd Macro_Dashboard
streamlit run dashboard.py

---

# Capital Markets Lab

A live macro and commodities analytics platform built with Python and Streamlit.

🔗 [Live Dashboard](https://capital-markets-labs.streamlit.app/)

## Pages
- **Macro Dashboard** — Price history, rolling volatility, correlation matrix, live market signals, and dynamic trade ideas across WTI, Brent, Nat Gas, USD Index, and 10Y Yield
- **Crude Spread Model** — Brent-WTI spread analysis, Z-score mean reversion signals, and live trade signals
