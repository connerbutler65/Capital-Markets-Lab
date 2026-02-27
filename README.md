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
