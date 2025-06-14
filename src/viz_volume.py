import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

def build_polar_volume_chart(df, events, ticker, rolling_window=7):
    """
    Construit un graphique polaire des volumes journaliers avec événements marqués.
    
    Parameters:
    df: DataFrame avec dates en index, tickers en colonnes
    events: liste des événements 
    ticker: nom du ticker sélectionné
    rolling_window: fenêtre de lissage
    """
    
    # Vérifier que le ticker existe
    if ticker not in df.columns:
        available_tickers = [col for col in df.columns if not col.endswith(('_return', '_volatility'))]
        print(f"Ticker {ticker} non trouvé. Tickers disponibles: {available_tickers}")
        
        # Retourner un graphique vide avec message d'erreur
        fig = go.Figure()
        fig.add_annotation(
            text=f"Données non disponibles pour {ticker}",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title=f"Volume journalier - {ticker}",
            showlegend=False
        )
        return fig
    
    # Extraire les données du ticker sélectionné
    ticker_data = df[ticker].dropna().copy()
    
    if len(ticker_data) == 0:
        # Retourner un graphique vide si pas de données
        fig = go.Figure()
        fig.add_annotation(
            text=f"Aucune donnée valide pour {ticker}",
            x=0.5, y=0.5,
            xref="paper", yref="paper", 
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(title=f"Volume journalier - {ticker}")
        return fig
    
    # Convertir en DataFrame pour faciliter les calculs
    data = pd.DataFrame({
        'Date': ticker_data.index,
        'Volume': ticker_data.values
    })
    
    # Appliquer le lissage
    if rolling_window > 1:
        data['Volume_smooth'] = data['Volume'].rolling(
            window=rolling_window, 
            center=True,
            min_periods=1
        ).mean()
    else:
        data['Volume_smooth'] = data['Volume']
    
    # Ajouter les informations temporelles pour le graphique polaire
    data['Month'] = data['Date'].dt.month
    data['Day_of_year'] = data['Date'].dt.dayofyear
    data['Year'] = data['Date'].dt.year
    
    # Calculer l'angle pour chaque point (0-360°, basé sur le jour de l'année)
    data['Angle'] = (data['Day_of_year'] / 365.25) * 360
    
    # Créer le graphique polaire
    fig = go.Figure()
    
    # Ajouter les données de volume comme trace polaire
    fig.add_trace(go.Scatterpolar(
        r=data['Volume_smooth'],
        theta=data['Angle'],
        mode='lines+markers',
        name=f'Volume {ticker}',
        line=dict(color='rgba(0, 168, 255, 0.8)', width=2),
        marker=dict(size=3, color='rgba(0, 168, 255, 0.6)'),
        hovertemplate=(
            f"<b>{ticker}</b><br>" +
            "Date: %{customdata}<br>" +
            "Volume: %{r:,.0f}<br>" +
            "<extra></extra>"
        ),
        customdata=data['Date'].dt.strftime('%Y-%m-%d')
    ))
    
    # Ajouter les événements comme points spéciaux
    event_colors = ['red', 'orange', 'purple', 'green', 'brown', 'pink', 'gray', 'cyan']
    
    for i, event in enumerate(events):
        event_date = pd.to_datetime(event['date'])
        
        # Trouver le point de données le plus proche de l'événement
        closest_idx = (data['Date'] - event_date).abs().idxmin()
        
        if closest_idx in data.index:
            closest_data = data.loc[closest_idx]
            
            # Vérifier que l'événement est dans la plage temporelle des données
            time_diff = abs((closest_data['Date'] - event_date).days)
            
            if time_diff <= 30:  # Afficher seulement si l'événement est dans les 30 jours des données
                fig.add_trace(go.Scatterpolar(
                    r=[closest_data['Volume_smooth']],
                    theta=[closest_data['Angle']],
                    mode='markers',
                    name=event['name'],
                    marker=dict(
                        size=12,
                        color=event_colors[i % len(event_colors)],
                        symbol='star'
                    ),
                    hovertemplate=(
                        f"<b>{event['name']}</b><br>" +
                        f"Date: {event_date.strftime('%Y-%m-%d')}<br>" +
                        f"Volume: {closest_data['Volume_smooth']:,.0f}<br>" +
                        "<extra></extra>"
                    )
                ))
    
    # Configuration du layout polaire
    fig.update_layout(
        title=dict(
            text=f"Volume journalier - {ticker} (Lissage: {rolling_window} jours)",
            x=0.5,
            font=dict(size=16)
        ),
        polar=dict(
        bgcolor="rgba(240, 240, 240, 0.1)",
        radialaxis=dict(
            title="Volume d'échange",
            gridcolor="rgba(0,0,0,0.1)",
            linecolor="rgba(0,0,0,0.2)"
        ),
        angularaxis=dict(
            # title supprimé car non supporté pour angularaxis
            tickmode="array",
            tickvals=[0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330],
            ticktext=["Jan", "Fév", "Mar", "Avr", "Mai", "Jun", 
                    "Jul", "Aoû", "Sep", "Oct", "Nov", "Déc"],
            gridcolor="rgba(0,0,0,0.1)",
            linecolor="rgba(0,0,0,0.2)",
            direction="clockwise",
            rotation=90
        )
    ),

        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left", 
            x=1.05
        ),
        margin=dict(l=80, r=120, t=80, b=80),
        height=600
    )
    
    return fig
