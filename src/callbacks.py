from dash.dependencies import Input, Output
from viz_volume import build_polar_volume_chart
from viz_heatmap import build_heatmap
from viz_volatility import build_volatility_chart
from viz_choropleth import build_choropleth
from viz_compare import build_compare_chart


def register_callbacks(app, df, events, regions_map):
    """
    Enregistre tous les callbacks de l'application.
    """
    
    # ======================= CALLBACK VISU 1: VOLUME POLAIRE =======================
    @app.callback(
        Output('volume-chart', 'figure'), 
        Output('window-value', 'children'), 
        Input('ticker-dropdown','value'), 
        Input('window-slider', 'value')
    ) 
    def update_volume_chart(ticker, rolling_window): 
        fig = build_polar_volume_chart(df, events, ticker, rolling_window)
        return fig, f"{int(rolling_window)} jours"

# ======================= CALLBACK VISU 2: HEATMAP DES RENDEMENTS =======================
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

# ======================= CALLBACK VISU 3: VOLATILITÉ =======================
    @app.callback(
        Output('volatility-chart', 'figure'),
        Input('volatility-event-dropdown', 'value'),
        Input('volatility-window-slider', 'value'),
        Input('volatility-grouping-dropdown', 'value')
    )
    def update_volatility(selected_event, window_days, grouping):
        """Met à jour le graphique de volatilité avec fenêtre adaptative."""
        rolling_window = max(3, window_days)
        
        if not selected_event:
            return build_volatility_chart(df, events, events[0]['name'], window_days, rolling_window, grouping)
        return build_volatility_chart(df, events, selected_event, window_days, rolling_window, grouping)
    
# ======================= CALLBACK VISU 4: CHOROPLETH =======================
    @app.callback(
        Output('choropleth-chart','figure'),
        Input('choro-event-dropdown','value'),
        Input('choro-window-slider','value')
    )
    def update_choropleth(event_name, post_window):
        return build_choropleth(df, events, event_name, regions_map, post_window=post_window)


# ======================= CALLBACK VISU 5: COMPARAISON DES CRISES =======================
    @app.callback(
        Output('compare-chart', 'figure'),
        Input('compare-category-dropdown', 'value'),
        Input('compare-mode-radio', 'value'),
        Input('compare-window-slider', 'value')
    )
    def update_compare(selected_category, mode, window_days):
        """Met à jour la comparaison selon la catégorie, métrique et fenêtre."""
        if not selected_category:
            # Récupérer la première catégorie disponible
            categories = list(set([e.get("category", "Autre") for e in events if e.get("category")]))
            selected_category = categories[0] if categories else "Géopolitique"
        
        return build_compare_chart(df, events, selected_category, window_days, mode)

