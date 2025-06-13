import plotly.express as px
import pandas as pd
import pycountry
import pycountry_convert as pc

def build_choropleth(df, events, event_name, region_map, post_window=5, range_color=[-1,1]):
    """
    df doit contenir 'Date','Ticker','ret'.
    region_map = {'Americas':[...], 'Europe':[...], 'Asia':[...]}.
    """
    
