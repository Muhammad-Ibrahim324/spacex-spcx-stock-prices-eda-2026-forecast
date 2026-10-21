from pathlib import Path
import argparse, hashlib, json
import pandas as pd
import numpy as np

def clean(source, destination):
    source, destination = Path(source), Path(destination)
    lines = source.read_text(encoding="utf-8-sig").splitlines()
    assert lines[0] == "Price,Close,High,Low,Open,Volume", "Unexpected source header"
    assert lines[1] == "Ticker,SPCX,SPCX,SPCX,SPCX,SPCX", "Unexpected ticker"
    assert lines[2] == "Date,,,,,", "Unexpected date metadata"
    df = pd.read_csv(source, skiprows=[1, 2]).rename(columns={"Price":"date"})
    df.columns = df.columns.str.lower()
    input_rows = len(df)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='raise')
    for col in ['open','high','low','close','volume']:
        df[col] = pd.to_numeric(df[col], errors='raise')
    assert not df.isna().any().any(), "Missing values require review"
    assert np.isfinite(df[['open','high','low','close','volume']]).all().all()
    duplicate_rows = int(df.duplicated().sum())
    df = df.drop_duplicates().sort_values('date').reset_index(drop=True)
    assert df.date.is_unique, "Conflicting duplicate dates require manual review"
    assert (df[['open','high','low','close']] > 0).all().all()
    assert (df.volume >= 0).all() and (df.volume % 1 == 0).all()
    assert (df.high >= df[['open','low','close']].max(axis=1)).all()
    assert (df.low <= df[['open','high','close']].min(axis=1)).all()
    prices=['open','high','low','close']
    rounding_error=float((df[prices]-df[prices].round(2)).abs().max().max())
    df[prices]=df[prices].round(2)
    df['volume']=df.volume.astype('int64')
    df.insert(1,'ticker','SPCX')
    df=df[['date','ticker','open','high','low','close','volume']]
    destination.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(destination,index=False,date_format='%Y-%m-%d',float_format='%.2f')
    audit={'source_file':source.name,'raw_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
           'input_price_rows':input_rows,'output_rows':len(df),'exact_duplicates_removed':duplicate_rows,
           'missing_values':int(df.isna().sum().sum()),'max_price_rounding_change_usd':rounding_error,
           'start_date':str(df.date.min().date()),'end_date':str(df.date.max().date()),
           'adjustment_status':'Unknown: source export does not record auto_adjust setting',
           'collection_timestamp':'Not supplied','source_version':'Not supplied',
           'clean_sha256':hashlib.sha256(destination.read_bytes()).hexdigest()}
    return audit

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='Flatten and validate the supplied SPCX yfinance export.')
    parser.add_argument('--input',default='data/raw/spcx_yfinance_original.csv')
    parser.add_argument('--output',default='data/spcx_daily_clean.csv')
    parser.add_argument('--audit',default='reports/cleaning_audit.json')
    args=parser.parse_args()
    audit=clean(args.input,args.output)
    Path(args.audit).parent.mkdir(parents=True,exist_ok=True)
    Path(args.audit).write_text(json.dumps(audit,indent=2)+'\n')
    print(json.dumps(audit,indent=2))
