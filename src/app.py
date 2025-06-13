import json
from pathlib import Path

import os

import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

from data_loader import load_market_data
from data_processor import compute_daily_returns, compute_volatility
from viz_volume import build_polar_volume_chart
from viz_heatmap import build_heatmap
from viz_volatility import build_volatility_chart
from viz_choropleth import build_choropleth
from viz_compare import build_compare_chart

# 1) Chargement des données et pré‐traitements
df = load_market_data()
df = compute_daily_returns(df)
df = compute_volatility(df)

# 2) Configurations (événements + mappings)
with open("config/events.json", "r") as f:
    events = json.load(f)
with open("config/tickers.json", "r") as f:
    cfg = json.load(f)

for ev in events:
    ev['date'] = pd.to_datetime(ev['date'])

regions_map       = cfg["regions"]
asset_classes_map = cfg["asset_classes"]
tickers_list      = sorted({t for sub in regions_map.values() for t in sub})
events_list       = [e["name"] for e in events]


# 3) Application Dash
app = dash.Dash(__name__)
server = app.server


app.layout = html.Div(
    style={'maxWidth':'900px','margin':'auto','padding':'20px'},
    children=[

        # Titre principal
        html.H1(
            "Impact des événements socio-politiques (2008–2023)",
            style={'textAlign':'center','marginBottom':'40px'}
        ),

    html.Div(className='viz-section', children=[

        html.H2("Volume d'échange (diagramme polaire)"),

        html.Div(className='control-group',
                 style={'marginBottom':'20px'},
                 children=[

            # Choix de l'indice
            html.Div(style={'display':'flex','alignItems':'center','gap':'10px'}, children=[
                html.Label("Indice :", style={'whiteSpace':'nowrap'}),
                dcc.Dropdown(
                    id='ticker-dropdown',
                    options=[{'label': t, 'value': t} for t in tickers_list],
                    value=tickers_list[0],
                    clearable=False,
                    style={'width':'160px'}
                ),
            ]),

            # Slider fenêtre glissante + affichage de valeur
            html.Div(style={'display':'flex','alignItems':'center','gap':'10px'}, children=[
                html.Label("Fenêtre glissante :", style={'whiteSpace':'nowrap'}),
                dcc.Slider(
                    id='window-slider',
                    min=1, max=30, step=1, value=7,
                    marks={i: str(i) for i in [1,3,7,14,30]},
                    tooltip={'placement':'bottom', 'always_visible':False},
                    updatemode='drag'
                ),
                html.Span(id='window-value', style={'minWidth':'50px','fontWeight':'bold'})
            ]),

        ]),

        dcc.Graph(id='volume-chart')

    ])

    ]  
)  

# 4) Callbacks
# --- callback pour Visu 0 ---

@app.callback( Output('volume-chart', 'figure'), 
              Output('window-value', 'children'), 
              Input('ticker-dropdown','value'), 
              Input('window-slider', 'value'), 
              ) 
def update_volume_chart(ticker, rolling_window): 
    """ Renvoie la figure polaire et la chaîne affichant la fenêtre choisie. """ 
    fig = build_polar_volume_chart(df, events, ticker, rolling_window) # on force int() pour éviter les .0 
    return fig, f"{int(rolling_window)} jours"

# 5) Lancement
if __name__ == '__main__':
    app.run_server(debug=True)


    '''
        # --- Visu 1 : heatmap des rendements
        html.Div(className='viz-section', children=[
            html.H2("Heatmap des rendements"),
            dcc.Dropdown(
                id='heatmap-event-dropdown',
                options=[{'label': n, 'value': n} for n in events_list],
                value=events_list[0],
                clearable=False,
                style={'width':'300px'}
            ),
            dcc.Graph(id='heatmap-chart')
        ]),

        # --- Visu 2 : volatilité glissante
        html.Div(className='viz-section', children=[
            html.H2("Volatilité glissante"),
            dcc.Dropdown(
                id='vol-event-dropdown',
                options=[{'label': n, 'value': n} for n in events_list],
                value=events_list[0],
                clearable=False,
                style={'width':'300px'}
            ),
            dcc.RadioItems(
                id='vol-grouping',
                options=[
                    {'label':'Régions',           'value':'regions'},
                    {'label':'Classes d’actif',   'value':'asset_classes'}
                ],
                value='regions',
                inline=True,
                style={'margin':'10px 0'}
            ),
            dcc.Graph(id='volatility-chart')
        ]),

        # --- Visu 3 : carte choropleth
        html.Div(className='viz-section', children=[
            html.H2("Carte choroplèthe régionale"),
            dcc.Dropdown(
                id='choro-event-dropdown',
                options=[{'label': n, 'value': n} for n in events_list],
                value=events_list[0],
                clearable=False,
                style={'width':'300px'}
            ),
            dcc.Graph(id='choropleth-chart')
        ]),

        # --- Visu 4 : comparaison Actions vs Matières premières
        html.Div(className='viz-section', children=[
            html.H2("Comparaison Actions vs Matières premières"),
            dcc.Dropdown(
                id='cmp-event-dropdown',
                options=[{'label': n, 'value': n} for n in events_list],
                value=events_list[0],
                clearable=False,
                style={'width':'300px'}
            ),
            dcc.RadioItems(
                id='cmp-metric',
                options=[
                    {'label':'Rendement',  'value':'return'},
                    {'label':'Volatilité', 'value':'volatility'}
                ],
                value='return',
                inline=True,
                style={'margin':'10px 0'}
            ),
            dcc.Graph(id='compare-chart')
        ])
        '''

'''

# --- callback pour Visu 1 ---
@app.callback(
    Output('heatmap-chart','figure'),
    Input('heatmap-event-dropdown','value')
)
def update_heatmap(ev):
    return build_heatmap(df, events, ev)

# --- callback pour Visu 2 ---
@app.callback(
    Output('volatility-chart','figure'),
    Input('vol-event-dropdown','value'),
    Input('vol-grouping','value')
)
def update_vol(ev, grouping):
    grp_map = regions_map if grouping=='regions' else asset_classes_map
    return build_volatility_chart(df, events, ev, window=7, grouping_map=grp_map)

# --- callback pour Visu 3 ---
@app.callback(
    Output('choropleth-chart','figure'),
    Input('choro-event-dropdown','value')
)
def update_choro(ev):
    return build_choropleth(df, events, ev, region_map=regions_map, post_window=5)

# --- callback pour Visu 4 ---
@app.callback(
    Output('compare-chart','figure'),
    Input('cmp-event-dropdown','value'),
    Input('cmp-metric','value')
)
def update_compare(ev, metric):
    return build_compare_chart(df, events, ev, asset_classes_map, window=5, metric=metric)

    
    '''


    
