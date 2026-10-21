# Kaggle publishing copy

Author: **Muhammad Ibrahim Shahrukh**

## Dataset title — 42 characters
SpaceX (SPCX) Historical Stock Prices 2026

## Subtitle — 74 characters
Daily OHLCV data with interactive EDA, risk analysis and 2026 ML forecasts

## Notebook title — 39 characters
SpaceX SPCX: EDA & 2026 Price Forecasts

## Dataset description
Explore SpaceX (SPCX) historical daily stock prices with a clean, beginner-friendly CSV covering June 12–October 19, 2026. The dataset contains 89 trading sessions and seven clearly named columns: date, ticker, open, high, low, close and volume. Prices are expressed in US dollars and volume in shares. The uploader obtained the source export from Yahoo Finance through the Python yfinance library.

The companion notebook walks through candlestick and volume charts, daily returns, drawdowns, rolling volatility, monthly performance, weekday distributions, correlations and return autocorrelation. It compares compact machine-learning models with transparent statistical baselines using expanding-window validation and a separate chronological holdout, then produces conditional price forecasts through December 31, 2026.

This snapshot is suitable for practicing pandas, financial visualization, time-series feature engineering, model evaluation and reproducible research. It is not live market data. Adjustment settings and the original download timestamp were not provided, so returns should not be interpreted as verified total returns. Forecasts and scenario bands are model outputs, not observed prices or guaranteed outcomes.

## CSV file description
`spcx_daily_clean.csv` contains 89 daily SpaceX (SPCX) OHLCV observations from June 12 through October 19, 2026. Each row represents one trading session with a date, ticker, opening price, session high, session low, closing price and share volume. The yfinance export was flattened into a single header, sorted by date, checked for duplicates, missing values and invalid OHLC relationships, and formatted with two-decimal prices and integer volumes. No missing prices were filled and no historical observations were synthesized.

## Column descriptions
| Column | Description (1–5 words) | Type | Unit |
|---|---|---|---|
| `date` | Trading session date | Date | YYYY-MM-DD |
| `ticker` | Stock ticker symbol | Text | SPCX |
| `open` | Opening share price | Decimal | USD per share |
| `high` | Highest session price | Decimal | USD per share |
| `low` | Lowest session price | Decimal | USD per share |
| `close` | Closing share price | Decimal | USD per share |
| `volume` | Shares traded | Integer | Shares |

## Suggested tags
Finance, Stock Market, Time Series, Exploratory Data Analysis, Machine Learning, Data Visualization, Forecasting, Python.

## Source attribution
Source: [Yahoo Finance — SPCX historical data](https://finance.yahoo.com/quote/SPCX/history/), downloaded by the uploader using [yfinance](https://github.com/ranaroussi/yfinance). Cleaned and documented by Muhammad Ibrahim Shahrukh. Data snapshot ends October 19, 2026; original download timestamp and adjustment parameters were not supplied.

## Publishing checklist
1. Create the Kaggle dataset using `data/spcx_daily_clean.csv` only. Copy the title, subtitle, description and field descriptions above.
2. Add the source attribution and choose a license consistent with the rights you have. See `DATA_LICENSE_NOTES.md`; this package does not assert an open-data license.
3. Create or import the notebook from `spcx_eda_2026_forecast.ipynb` and attach the newly created dataset via Add Input.
4. Run all cells. The loader searches `/kaggle/input` recursively for `spcx_daily_clean.csv`; set `DATA_PATH` if multiple copies are attached.
5. Keep forecasts separate from the historical dataset. Generated results appear in `/kaggle/working/spcx_outputs`.
6. Review notebook output, then save a version. Good presentation and transparency can help readers, but rankings and upvotes cannot be guaranteed.
