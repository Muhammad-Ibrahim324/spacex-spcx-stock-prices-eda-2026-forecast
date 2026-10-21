# SpaceX (SPCX) Historical Stock Prices 2026

**Interactive EDA, transparent evaluation and conditional year-end forecasts.**  
**Author: Muhammad Ibrahim Shahrukh**

This project makes an uploader-provided yfinance export easy to explore and reuse. It contains an audited daily CSV, a colorful Jupyter notebook with 13 Plotly figures, explicit chronological model evaluation and a standalone browser report. The history covers **89 sessions, June 12–October 19, 2026**. It is a fixed snapshot, not a live price feed.

## Start here
- Dataset: [`data/spcx_daily_clean.csv`](data/spcx_daily_clean.csv)
- Notebook: [`spcx_eda_2026_forecast.ipynb`](spcx_eda_2026_forecast.ipynb)
- Data, provenance and methodology: [`DATASET_GUIDE.md`](DATASET_GUIDE.md)
- Kaggle title, subtitle and descriptions: [`KAGGLE_METADATA.md`](KAGGLE_METADATA.md)
- Standalone charts: download [`reports/spcx_interactive_report.html`](reports/spcx_interactive_report.html) and open it in a browser.
- Forecasts: [`reports/spcx_forecast_2026.csv`](reports/spcx_forecast_2026.csv)
- Cleaning and execution audits: [`reports/cleaning_audit.json`](reports/cleaning_audit.json), [`reports/execution_report.json`](reports/execution_report.json)
- Cover prompt: [`DATASET_COVER_PROMPT.md`](DATASET_COVER_PROMPT.md)

## Snapshot findings
| Measure | Result |
|---|---|
| Last supplied close | $147.96 |
| First-to-last close change | -8.07% |
| Maximum closing drawdown | -48.78% |
| Validation-selected model | LastClose |
| Selected holdout MAE / RMSE | $6.91 / $8.90 |
| Last-close baseline holdout MAE | $6.91 |
| December 31 conditional forecast | $147.96 |
| December 31 80% scenario range | $108.21–$211.05 |

The forecast covers 51 sessions, longer than the 10-session validation and 20-session test horizon. Scenario bands are not calibrated prediction intervals. Short IPO-era history and unknown price adjustment settings substantially limit interpretation. Read the notebook's discussion before using the outputs.

## Run locally
Use Python 3.11 or newer. From this project's root folder:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux instead:
# source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyterlab
```

Open the notebook and choose **Run All**. Core package versions used for the supplied execution are recorded in `requirements-tested.txt` and `reports/environment_versions.json`; `requirements.txt` defines broader compatible ranges. Results can vary with software versions.

For an automated run in an environment that permits Jupyter kernel sockets:
```bash
python scripts/run_notebook.py
```

## Run on Kaggle
1. Upload `data/spcx_daily_clean.csv` as your dataset.
2. Import `spcx_eda_2026_forecast.ipynb` and attach that dataset with Add Input.
3. Run all cells. No internet connection is required for analysis.
4. If the loader finds more than one copy, assign the exact CSV path to `DATA_PATH` in the setup cell.
5. Results are saved to `/kaggle/working/spcx_outputs`.

Every plot is displayed with **`fig.show(renderer="iframe")`**. Rerunning generates the iframe assets. GitHub does not reliably render notebook iframe output; download the standalone HTML report or run the notebook locally. The report embeds the Plotly runtime and needs no CDN. The ZIP also includes the generated `iframe_figures` for local viewing; git excludes these large reproducible files.

## What the notebook covers
Data integrity; source caveats; KPI cards; candlesticks and volume; moving averages; daily returns; drawdown; rolling volatility; histograms and Q–Q diagnostics; monthly and weekday analysis; return/volume associations; correlations; autocorrelation; validation ranking; holdout paths and forecast errors; illustrative feature importance; and year-end scenario bands.

## Model design
Eight candidates: last-close, log drift, damped drift, three Ridge configurations, Random Forest and Extra Trees. ML predicts log returns from past-return features and compounds them recursively. Expanding training windows of 39/49/59 rows each forecast the next 10 sessions. Mean validation price MAE selects the model, with RMSE as tie-break. The final 20 sessions are held out once; the winner is not changed based on test rankings. Final refitting uses all 89 observations.

Errors include MAE, RMSE, MAPE, MASE, R² and origin-relative direction agreement. The scenario generator uses 4,000 centered moving-block return paths with seed 42. It checks coverage at the holdout origin for transparency, not proof of calibration. See the guide for exact assumptions and limitations.

## Reproduce cleaning
The complete ZIP preserves the original file at `data/raw/spcx_yfinance_original.csv`. It is excluded from git by default. If working from a GitHub clone, supply that original export before running:

```bash
python scripts/clean_data.py
```

The cleaner checks the exact source schema, removes metadata rows, parses and sorts data, rejects conflicting duplicates and invalid values, rounds OHLC to cents and preserves volume as integer shares. It writes a SHA-256 audit. No source observations were removed from this snapshot.

## Verification
All code cells were executed sequentially from the `.ipynb` in a fresh in-process IPython session, with outputs saved back into the notebook. No cell errors remained and 13 iframe outputs were generated. The environment could not open the sockets required for a separate Jupyter kernel; Kaggle's UI was not directly tested. See `reports/execution_report.json`. The supplied automated runner uses a normal notebook kernel on your machine or Kaggle.

## Data source and rights
The uploader reports collecting the data from [Yahoo Finance](https://finance.yahoo.com/quote/SPCX/history/) using [yfinance](https://github.com/ranaroussi/yfinance). The original download parameters and adjustment settings are unknown. Nasdaq confirms the [SpaceX SPCX listing](https://www.nasdaq.com/newsroom/spacex-ipo-rocket-company-launches-historic-ipo); forecast dates follow its [2026 calendar](https://nasdaqtrader.com/Trader.aspx?id=Calendar). Individual historical bars have not been independently reconciled.

No open-data license is asserted. Software licensing and market-data redistribution rights are separate. Review [`DATA_LICENSE_NOTES.md`](DATA_LICENSE_NOTES.md) before publishing. The dataset is educational; forecasts are not investment advice or guaranteed returns.

## Suggested citation
Muhammad Ibrahim Shahrukh (2026). *SpaceX (SPCX) Historical Stock Prices 2026*. Snapshot June 12–October 19, 2026. Yahoo Finance data accessed by the uploader through yfinance; cleaning, analysis and documentation by Muhammad Ibrahim Shahrukh. Add the published dataset/repository URL after upload.

## Contributions
Useful contributions include documented data updates, corporate-action verification, longer walk-forward evaluations and rendering fixes. Report your package versions and reproducible steps for issues. Do not add API keys, personal tokens or forecasts disguised as observed records.
