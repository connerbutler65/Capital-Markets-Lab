# Capital Markets Lab

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

## Setup

```bash
pip install -r requirements.txt
cd Macro_Dashboard
streamlit run dashboard.py

---

## Project 2: Crude Oil Spread Model & Backtest

A quantitative research tool analyzing the Brent-WTI crude oil spread using 
statistical signals and systematic trading strategies.

**Assets tracked:** Brent Crude (BZ=F), WTI Crude (CL=F)

**Features:**
- Live Brent-WTI spread calculation and classification
- 30-day rolling Z-score to identify statistically extreme spread levels
- Backtested mean reversion strategy (Z-score signal)
- Backtested momentum strategy (moving average crossover)
- Comparative strategy analysis across 2 years of data

**Key Finding:**
Neither mean reversion (-$14.25 P&L) nor momentum (-$14.99 P&L) generated 
positive returns on the Brent-WTI spread over the 2024-2026 period. 
The spread appears driven by structural supply factors (Cushing storage, 
pipeline capacity, geopolitics) rather than statistical price patterns alone.
Future work: incorporate EIA crude inventory data as a fundamental signal layer.

**Current Signal (Feb 27 2026):**
- Spread: $5.88 (Brent Premium)
- Z-Score: 2.22 — spread is 2.2 standard deviations above its 30-day average

**Data Source:** Yahoo Finance (yfinance)

**Tech Stack:** Python, Pandas, yfinance
