import pandas as pd
import json
from datetime import timedelta

# Charger la config
with open("config/tickers.json") as f:
    _CFG = json.load(f)

def compute_daily_returns(df):
    """Ajoute la colonne 'ret' = variation journalière des cours."""
    df = df.copy()
    df['ret'] = df.groupby('Ticker')['Close'].pct_change()
    return df

def compute_volatility(df, window=5):
    """Ajoute la colonne 'vol' = écart-type glissant des rendements."""
    df = df.copy()
    df['vol'] = (
        df.groupby('Ticker')['ret']
          .rolling(window=window, min_periods=1)
          .std()
          .reset_index(level=0, drop=True)
    )
    return df

def get_event_window(df, event_date, pre=5, post=5):
    """
    Filtre df pour ne garder que [event_date-pre … event_date+post].
    Renvoie une copie avec la colonne day_rel.
    """
    df = df.copy()
    start = pd.to_datetime(event_date) - timedelta(days=pre)
    end   = pd.to_datetime(event_date) + timedelta(days=post)
    mask  = (df['Date'] >= start) & (df['Date'] <= end)
    win   = df.loc[mask].copy()
    win['day_rel'] = (win['Date'] - pd.to_datetime(event_date)).dt.days
    return win

def aggregate_region_returns(df_win, region_key="regions"):
    """
    Agrège les retours moyens par continent d'après le mapping config/tickers.json.
    Renvoie DataFrame [region, mean_return].
    """
    rows = []
    for region, tickers in _CFG.get(region_key,{}).items():
        sub = df_win[df_win['Ticker'].isin(tickers)]
        mean_r = sub['ret'].mean() * 100
        rows.append({'region': region, 'mean_return': mean_r})
    return pd.DataFrame(rows)
