# SpaceX SPCX dataset guide

**Author:** Muhammad Ibrahim Shahrukh  
**Documentation date:** October 20, 2026  
**Observed period:** June 12–October 19, 2026  
**Frequency:** One row per scheduled trading session  
**Currency:** USD  
**Rows / columns:** 89 / 7

## What is this dataset?
Explore SpaceX (SPCX) historical daily stock prices with a clean, beginner-friendly CSV covering June 12–October 19, 2026. The dataset contains 89 trading sessions and seven clearly named columns: date, ticker, open, high, low, close and volume. Prices are expressed in US dollars and volume in shares. The uploader obtained the source export from Yahoo Finance through the Python yfinance library.

The companion notebook walks through candlestick and volume charts, daily returns, drawdowns, rolling volatility, monthly performance, weekday distributions, correlations and return autocorrelation. It compares compact machine-learning models with transparent statistical baselines using expanding-window validation and a separate chronological holdout, then produces conditional price forecasts through December 31, 2026.

This snapshot is suitable for practicing pandas, financial visualization, time-series feature engineering, model evaluation and reproducible research. It is not live market data. Adjustment settings and the original download timestamp were not provided, so returns should not be interpreted as verified total returns. Forecasts and scenario bands are model outputs, not observed prices or guaranteed outcomes.

## Data dictionary
| Column | Description (1–5 words) | Type | Unit |
|---|---|---|---|
| `date` | Trading session date | Date | YYYY-MM-DD |
| `ticker` | Stock ticker symbol | Text | SPCX |
| `open` | Opening share price | Decimal | USD per share |
| `high` | Highest session price | Decimal | USD per share |
| `low` | Lowest session price | Decimal | USD per share |
| `close` | Closing share price | Decimal | USD per share |
| `volume` | Shares traded | Integer | Shares |

`date` is a session label, not a timestamp; no timezone is encoded in the CSV. Price fields preserve the source's unknown adjustment basis. No `adj_close`, dividend or split columns are present. USD units are consistent with Yahoo's SPCX quote page; the original CSV itself does not carry currency metadata.

## Provenance and collection methodology
The source chain is **Yahoo Finance → yfinance → uploader's CSV → this cleaned snapshot**. The uploader described the collection tool as yfinance. The raw file has a field header (`Price,Close,High,Low,Open,Volume`), a ticker header and a date-label row, consistent with a pandas MultiIndex CSV exported from yfinance. This is observed format evidence; it is not a recovery of the exact download command.

The original collection time, yfinance version, requested start/end arguments, interval settings, adjustment options, repair settings and timezone settings were not supplied. The daily frequency is evident in the session dates. We did not re-download, extend, merge or silently revise the uploaded values. Individual bars have not been independently checked against an exchange feed. The source history page could not be retrieved during independent review because it returned HTTP 429; identity was checked against Nasdaq and Yahoo's quote listing.

The source starts on June 12, 2026, consistent with [Nasdaq's SpaceX listing report](https://www.nasdaq.com/newsroom/spacex-ipo-rocket-company-launches-historic-ipo). Security identity must be checked before joining older files: a ticker string alone is not a permanent security identifier.

### Transparent future collection example
The following is a **proposed explicit collection recipe**, not the undisclosed command used to create the attachment. It is not executed by the analysis notebook. A new download can differ due to provider revisions or a different adjustment basis.

```python
from pathlib import Path
from datetime import datetime, timezone
import json
import yfinance as yf

params = dict(tickers='SPCX', start='2026-06-12', end='2026-10-20',
              interval='1d', auto_adjust=False, back_adjust=False,
              actions=False, repair=False, prepost=False,
              multi_level_index=True, progress=False)
download = yf.download(**params)  # start inclusive, end exclusive
download.to_csv('spcx_new_download.csv')
Path('collection_metadata.json').write_text(json.dumps({
    'retrieved_at_utc': datetime.now(timezone.utc).isoformat(),
    'yfinance_version': yf.__version__, 'parameters': params
}, indent=2))
```

This recipe explicitly requests unadjusted OHLC and may include an adjusted-close field. The supplied-file cleaner intentionally accepts only the original six-field export; adapt and document a separate schema for future downloads instead of dropping new fields silently.

## Transformation log
| Step | Transformation | Result |
|---|---|---|
| 1 | Preserve source bytes | Raw SHA-256 recorded below |
| 2 | Flatten field/ticker header | One conventional header |
| 3 | Rename and order columns | `date,ticker,open,high,low,close,volume` |
| 4 | Parse dates and numbers strictly | Invalid values would stop processing |
| 5 | Sort by session date | Ascending date order |
| 6 | Remove exact duplicate rows | 0 removed |
| 7 | Reject conflicting duplicate dates | None found |
| 8 | Validate missing, finite and OHLC values | All 89 rows retained |
| 9 | Round price fields to cents | Largest change $0.0000073242 |
| 10 | Store volume as integer shares | No scaling or imputation |
| 11 | Compare with 2026 Nasdaq session calendar | No missing or unexpected sessions |

All observations survived cleaning. No forward fill, backfill, interpolation, winsorization, outlier removal, resampling, currency conversion or new corporate-action adjustment was applied. Rounding deliberately removes binary floating-point export noise; it must not be confused with undoing an adjustment. The raw file remains available if greater numerical fidelity is needed.

- Original SHA-256: `a92cb86a60a486d5dfe3667ba31eeddcdadee8670bd5f27eba9039314a82a40e`
- Clean CSV SHA-256: `cf6f8dbaef2b259fdc98ce83db2f314bb9350d2b95f69a3578675ab1a66a0c11`

## Beginner quick start
```python
import pandas as pd
df = pd.read_csv('data/spcx_daily_clean.csv', parse_dates=['date'])
print(df.head())
print(df.describe())
df['daily_return_pct'] = df['close'].pct_change(fill_method=None) * 100
```
The first return is missing by definition because there is no prior close. Do not turn that missing return into an observed zero. A 20-session rolling volatility needs 20 returns, so early derived values are also intentionally missing. The historical CSV itself has no missing values.

## EDA method
Validate schema and trading sessions before calculating changes. Examine OHLC candles with volume; then separate daily returns, drawdown and rolling volatility. Check the return distribution and a normal Q–Q reference for tails. Compare partial-period monthly returns, weekday samples, volume versus absolute return, Spearman correlations among changes and return autocorrelation. Each visual includes limits on interpretation. Level correlations, seasonal conclusions and annualized growth claims are avoided because the history is short.

## Modeling and evaluation
Eight candidates include random walk, log drift, damped drift, Ridge with alpha 1/10/100, Random Forest and Extra Trees. ML targets next-session log returns using nine past-return features. Return forecasts are compounded recursively without future actual prices. Scaling is fitted within the training window. No external news, same-day future OHLC or future volume enters the model.

The final 20 sessions are held out. The earlier 69 rows support three expanding training windows of 39, 49 and 59 rows, each followed by a non-overlapping 10-session validation block. Selection uses mean validation price MAE, with RMSE as a tie-break. The selected configuration stays fixed during the 20-session holdout and is subsequently refitted to all 89 rows. Full-history EDA is descriptive and separate from the fixed candidate selection rule; it is not a formal pre-registered study.

MAE/RMSE are in USD; MAPE is in percent. MASE scales MAE by the training one-step absolute price change. MAE skill compares to a same-origin last-close forecast. R² may be negative. Direction measures the sign of each future close relative to the forecast-origin close, not daily strategy accuracy. All metrics are descriptive of a small number of dependent forecast paths; no trading backtest or transaction-cost profitability claim is made.

## Forecast method and limitations
The final 51 dates run from October 20 to December 31, 2026. Weekends and the full closures on November 26 and December 25 are removed; early closes remain sessions. A fixed 2026 calendar is taken from Nasdaq Trader. Emergency closures are not anticipated. Forecast dates are anchored to the input snapshot, not the wall-clock date when the notebook is rerun.

The latest 60 log returns are centered and resampled in circular blocks of five, with 4,000 paths and seed 42. Accumulated shocks surround the selected deterministic price path. Percentile envelopes are pointwise scenario bands, not calibrated prediction intervals. They do not include full parameter, model, event or regime uncertainty. The model was validated at 10 sessions and tested at 20, so its 51-session horizon is an unvalidated extrapolation. A model that wins validation may still lose to a baseline later.

## Forecast CSV dictionary
| Column | Description |
|---|---|
| date | Forecast trading session |
| ticker | Stock ticker symbol |
| model | Validation-selected model |
| forecast_close | Conditional point forecast |
| scenario_low_80 | Tenth percentile scenario |
| scenario_high_80 | Ninetieth percentile scenario |
| scenario_low_95 | 2.5th percentile scenario |
| scenario_high_95 | 97.5th percentile scenario |
| forecast_origin | Last observed session |
| horizon_sessions | Sessions after forecast origin |

Forecast prices and scenario limits use USD per share and are stored to four decimals for numerical reproducibility, not because that precision is meaningful. Do not append them to the observed CSV as actual market data.

## Citation and source links
Suggested dataset citation: Muhammad Ibrahim Shahrukh (2026), *SpaceX (SPCX) Historical Stock Prices 2026*, snapshot June 12–October 19, 2026, derived from uploader-provided Yahoo Finance data via yfinance. Add the final Kaggle dataset URL and version after publication.

- [Yahoo Finance historical prices](https://finance.yahoo.com/quote/SPCX/history/)
- [Yahoo Finance SPCX quote](https://finance.yahoo.com/quote/SPCX/)
- [yfinance source and project notices](https://github.com/ranaroussi/yfinance)
- [yfinance download documentation](https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html)
- [Nasdaq listing context](https://www.nasdaq.com/newsroom/spacex-ipo-rocket-company-launches-historic-ipo)
- [Nasdaq 2026 trading calendar](https://nasdaqtrader.com/Trader.aspx?id=Calendar)
- [scikit-learn metrics](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [Plotly rendering documentation](https://plotly.com/python/renderers/)

Documentation reviewed October 20, 2026. See `DATA_LICENSE_NOTES.md` for redistribution limits. No open-data license is asserted by this package.
