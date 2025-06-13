import plotly.express as px
import pandas as pd

def build_volatility_chart(df, events, event_name, window=7, grouping_map=None):
    """
    df doit contenir 'Date','Ticker','vol' (volatilité glissante).
    grouping_map est dict {group_name: [tickers]}.
    """
   