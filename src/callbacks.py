from dash.dependencies import Input, Output
from viz_volume import build_polar_volume_chart
from viz_choropleth import build_choropleth

def register_callbacks(app, df, events, regions_map):
    """
    Enregistre tous les callbacks de l'application.
    """
    
    # === CALLBACK VISU 1: Volume polaire ===
    @app.callback(
        Output('volume-chart', 'figure'), 
        Output('window-value', 'children'), 
        Input('ticker-dropdown','value'), 
        Input('window-slider', 'value')
    ) 
    def update_volume_chart(ticker, rolling_window): 
        """Renvoie la figure polaire et la chaîne affichant la fenêtre choisie.""" 
        fig = build_polar_volume_chart(df, events, ticker, rolling_window)
        return fig, f"{int(rolling_window)} jours"

    # === CALLBACK VISU 4: Carte choroplèthe ===
    @app.callback(
        Output('choropleth-chart','figure'),
        Input('choro-event-dropdown','value'),
        Input('choro-window-slider','value')
    )
    def update_choropleth(event_name, post_window):
        """Met à jour la carte choroplèthe selon l'événement et la fenêtre."""
        return build_choropleth(df, events, event_name, regions_map, post_window=post_window)
