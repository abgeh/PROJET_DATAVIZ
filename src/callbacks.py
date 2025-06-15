from dash.dependencies import Input, Output
from viz_volume import build_polar_volume_chart
from viz_heatmap import build_heatmap
from viz_volatility import build_volatility_chart
from viz_choropleth import build_choropleth


def register_callbacks(app, df, events, regions_map):
    """
    Enregistre tous les callbacks de l'application.
    """
    
    # === CALLBACK VISU 1: Volume polaire === (existant)
    @app.callback(
        Output('volume-chart', 'figure'), 
        Output('window-value', 'children'), 
        Input('ticker-dropdown','value'), 
        Input('window-slider', 'value')
    ) 
    def update_volume_chart(ticker, rolling_window): 
        fig = build_polar_volume_chart(df, events, ticker, rolling_window)
        return fig, f"{int(rolling_window)} jours"

    # === CALLBACK VISU 2: Heatmap temporelle === (NOUVEAU)
    @app.callback(
        Output('heatmap-chart', 'figure'),
        Input('heatmap-event-dropdown', 'value'),
        Input('heatmap-window-slider', 'value')
    )
    def update_heatmap(selected_event, window_days):
        """Met à jour la heatmap selon l'événement et la fenêtre temporelle."""
        if not selected_event:
            return build_heatmap(df, events, events[0]['name'], window_days)
        return build_heatmap(df, events, selected_event, window_days)

    # === CALLBACK VISU 3: Volatilité === (AVEC FENÊTRE ADAPTATIVE)
    @app.callback(
        Output('volatility-chart', 'figure'),
        Input('volatility-event-dropdown', 'value'),
        Input('volatility-window-slider', 'value'),
        Input('volatility-grouping-dropdown', 'value')
    )
    def update_volatility(selected_event, window_days, grouping):
        """Met à jour le graphique de volatilité avec fenêtre adaptative."""
        # CORRIGÉ: Fenêtre mobile réellement adaptative
        rolling_window = max(3, window_days)
        
        if not selected_event:
            return build_volatility_chart(df, events, events[0]['name'], window_days, rolling_window, grouping)
        return build_volatility_chart(df, events, selected_event, window_days, rolling_window, grouping)
    
    # === CALLBACK VISU 4: Carte choroplèthe === (existant)
    @app.callback(
        Output('choropleth-chart','figure'),
        Input('choro-event-dropdown','value'),
        Input('choro-window-slider','value')
    )
    def update_choropleth(event_name, post_window):
        return build_choropleth(df, events, event_name, regions_map, post_window=post_window)


