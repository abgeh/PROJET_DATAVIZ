import plotly.express as px
import pandas as pd

def build_compare_chart(df, events, event_name, asset_classes_map, window=5, metric='return'):
    """
    df doit contenir 'Date','Ticker','ret','vol'.
    asset_classes_map = {'Actions':[...], 'Matières Premières':[...]}.
    """
 
