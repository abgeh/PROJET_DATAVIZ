import json
import pandas as pd
import dash
from dash import html

from data_loader import load_market_data
from data_processor import compute_daily_returns, compute_volatility
from layout_components import create_header, create_volume_section, create_heatmap_section, create_volatility_section, create_choropleth_section, create_compare_section
from callbacks import register_callbacks



# === 1) CHARGEMENT DES DONNÉES ===
df = load_market_data()
df = compute_daily_returns(df)
df = compute_volatility(df)

# === 2) CONFIGURATIONS ===
with open("config/events.json", "r") as f:
    events = json.load(f)
with open("config/tickers.json", "r") as f:
    cfg = json.load(f)

# Conversion des dates
for ev in events:
    ev['date'] = pd.to_datetime(ev['date'])

# Variables globales
regions_map = cfg["regions"]
tickers_list = sorted({t for sub in regions_map.values() for t in sub})
events_list = [e["name"] for e in events]

# Mapping spécifique pour la choroplèthe
regions_map = {
    'Americas': ['^GSPC', '^DJI', '^IXIC'],
    'Europe': ['^FTSE', '^GDAXI', '^FCHI'],
    'Asia': ['^N225', '000001.SS', '^NSEI']
}

# === 3) APPLICATION DASH ===
app = dash.Dash(__name__)
server = app.server

# Extraire les catégories uniques des événements
categories = sorted(set(ev["category"] for ev in events if "category" in ev))

# === 4) LAYOUT PRINCIPAL ===
app.layout = html.Div(
    style={'maxWidth':'900px','margin':'auto','padding':'20px'},
    children=[
        create_header(),
        create_volume_section(tickers_list),
        create_heatmap_section(events_list),
        create_volatility_section(events_list),  # NOUVEAU
        create_choropleth_section(events_list),
        create_compare_section(categories) 
    ]
)

# === 5) ENREGISTREMENT DES CALLBACKS ===
register_callbacks(app, df, events, regions_map)

# === 6) LANCEMENT ===
if __name__ == '__main__':
    app.run_server(debug=True)
