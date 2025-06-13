import plotly.express as px
import pandas as pd

def build_heatmap(df, events, event_name, window=7):
    """
    df doit contenir 'Date','Ticker','ret' (rendements).
    events = [{name,date},…], event_name est une des clés name.
    """
    