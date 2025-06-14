import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

def build_polar_volume_chart(df, events, ticker, rolling_window=7):
    """
    Graphique polaire chronologique - données dans l'ordre temporel correct.
    """
    
    # Vérifier que le ticker existe
    if ticker not in df.columns:
        available_tickers = [col for col in df.columns if not col.endswith(('_return', '_volatility'))]
        print(f"Ticker {ticker} non trouvé. Tickers disponibles: {available_tickers}")
        
        fig = go.Figure()
        fig.add_annotation(
            text=f"Données non disponibles pour {ticker}",
            x=0.5, y=0.5, xref="paper", yref="paper",
            showarrow=False, font=dict(size=16, color="red")
        )
        fig.update_layout(title=f"Volume journalier - {ticker}", showlegend=False)
        return fig
    
    # Extraire les données du ticker sélectionné
    ticker_data = df[ticker].dropna().copy()
    
    if len(ticker_data) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Aucune donnée valide pour {ticker}",
            x=0.5, y=0.5, xref="paper", yref="paper", 
            showarrow=False, font=dict(size=16, color="red")
        )
        fig.update_layout(title=f"Volume journalier - {ticker}")
        return fig
    
    # === LOGIQUE TEMPORELLE CHRONOLOGIQUE (VOTRE LOGIQUE - INCHANGÉE) ===
    data = pd.DataFrame({
        'Date': ticker_data.index,
        'Volume': ticker_data.values
    })
    
    data = data.sort_values('Date').reset_index(drop=True)
    
    if rolling_window > 1:
        data['Volume_smooth'] = data['Volume'].rolling(
            window=rolling_window, center=True, min_periods=1
        ).mean()
    else:
        data['Volume_smooth'] = data['Volume']
    
    # === CALCUL DES ANGLES CHRONOLOGIQUE  ===
    date_min = data['Date'].min()
    date_max = data['Date'].max()
    total_days = (date_max - date_min).days

    data['Days_from_start'] = (data['Date'] - date_min).dt.days
    data['Theta'] = (data['Days_from_start'] / total_days) * 360

    # Détecter et gérer les valeurs aberrantes
    Q1 = data['Volume_smooth'].quantile(0.25)
    Q3 = data['Volume_smooth'].quantile(0.75)
    IQR = Q3 - Q1
    upper_fence = Q3 + 2.5 * IQR  # Seuil des outliers

    outliers_mask = data['Volume_smooth'] > upper_fence
    outliers_count = outliers_mask.sum()

    if outliers_count > 0:
        # Utiliser une échelle logarithmique pour préserver les variations
        data['Volume_log'] = np.log1p(data['Volume_smooth'])  # log(1+x) pour éviter log(0)
        data['Radius'] = data['Volume_log'] / data['Volume_log'].max()  # Normaliser 0-1
        scale_info = f"échelle log, {outliers_count} outliers détectés"
    else:
        # Échelle linéaire normale
        data['Radius'] = data['Volume_smooth'] / data['Volume_smooth'].max()  # Normaliser 0-1
        scale_info = "échelle linéaire"


    
    # === CRÉATION DU GRAPHIQUE ===
    fig = go.Figure()
    
    # 1) TRACE DE REMPLISSAGE (VOTRE LOGIQUE - INCHANGÉE)
    if len(data) > 2:
        fill_angles = np.concatenate([[data['Theta'].iloc[0]], data['Theta'].values, [data['Theta'].iloc[-1]]])
        fill_radius = np.concatenate([[0], data['Radius'].values, [0]])
        
        fig.add_trace(go.Scatterpolar(
            r=fill_radius,
            theta=fill_angles,
            mode='lines',
            fill='toself',
            fillcolor='rgba(0, 128, 128, 0.2)',
            line=dict(color='rgba(0, 128, 128, 0)', width=0),
            showlegend=False,
            hoverinfo='skip',
            name='Remplissage'
        ))

    # 2) TRACE PRINCIPALE (ENHANCED BUT SAME LOGIC)
    fig.add_trace(go.Scatterpolar(
        r=data['Radius'],
        theta=data['Theta'],
        mode='lines+markers',
        name=f'Volume {ticker}',
        line=dict(color='teal', width=2),
        marker=dict(size=3, color='teal', opacity=0.7),
        hovertemplate=(
            f"<b>{ticker}</b><br>" +
            "📅 Date: %{customdata}<br>" +
            "📊 Volume: %{r:.2f}Md<br>" +
            "<extra></extra>"
        ),
        customdata=data['Date'].dt.strftime('%d/%m/%Y')
    ))

    # 3) REPÈRES ANNUELS (VOTRE LOGIQUE - INCHANGÉE)
# 3) REPÈRES ANNUELS (VERSION CORRIGÉE POUR SYNCHRONISATION)
    year_annotations = []
    years_in_data = sorted(data['Date'].dt.year.unique())

    for year in years_in_data:
        year_start = pd.Timestamp(f"{year}-01-01")
        if year_start < date_min:
            year_start = date_min
        elif year_start > date_max:
            continue
            
        days_from_start = (year_start - date_min).days
        angle_deg = (days_from_start / total_days) * 360
        
        # 🔧 CORRECTION : Ajuster pour correspondre à la config du graphique polaire
        # Le graphique a rotation=90 et direction="clockwise"
        # On doit ajuster l'angle pour que les annotations correspondent
        adjusted_angle_rad = np.radians(90 - angle_deg)  # Correction du décalage
        
        year_annotations.append(
            dict(
                x=0.5 + 0.47 * np.cos(adjusted_angle_rad),
                y=0.5 + 0.47 * np.sin(adjusted_angle_rad),
                text=str(year),
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=10, color="#2c3e50", family="Arial", weight="bold"),
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="#bdc3c7",
                borderwidth=1,
                borderpad=3
            )
        )

    # 4) ÉVÉNEMENTS GÉOPOLITIQUES (VOTRE LOGIQUE - INCHANGÉE)
    events_data = [
        {"name": "Crise 2008", "date": "2008-09-15"},
        {"name": "Printemps arabe", "date": "2011-01-25"},
        {"name": "Fukushima", "date": "2011-03-11"},
        {"name": "Brexit", "date": "2016-06-23"},
        {"name": "Trump élu", "date": "2016-11-08"},
        {"name": "Guerre Chine-USA", "date": "2018-07-06"},
        {"name": "Soleimani", "date": "2020-01-03"},
        {"name": "COVID-19", "date": "2020-03-11"},
        {"name": "Capitole", "date": "2021-01-06"},
        {"name": "Ukraine", "date": "2022-02-24"}
    ]

    max_radius = data['Radius'].max() if len(data) > 0 else 5

    for event in events_data:
        event_date = pd.to_datetime(event['date'])
        
        if event_date < date_min or event_date > date_max:
            continue
        
        days_from_start = (event_date - date_min).days
        event_theta = (days_from_start / total_days) * 360
        
        n_points = 20
        r_line = np.linspace(0, max_radius * 1.15, n_points)
        theta_line = np.full(n_points, event_theta)
        
        fig.add_trace(go.Scatterpolar(
            r=r_line,
            theta=theta_line,
            mode='lines+markers',
            line=dict(color='brown', width=1.5, dash='dash'),
            marker=dict(size=0.5, color='brown', opacity=0.3),
            showlegend=False,
            name=event['name'],
            hovertemplate=(
                f"<b>{event['name']}</b><br>" +
                f"Date: {event['date']}<br>" +
                "Événement géopolitique<br>" +
                "<extra></extra>"
            )
        ))

    # 5) CONFIGURATION DU LAYOUT (ENHANCED FOR PERFECT CENTERING)
    fig.update_layout(
        title=dict(
            text=f"Volume journalier - {ticker} (Lissage: {rolling_window} jours)",
            x=0.5,
            font=dict(size=16, color="#2c3e50")
        ),
        polar=dict(
            bgcolor="rgba(245, 245, 245, 0.3)",
            radialaxis=dict(
                title="Volume (Milliards)",
                gridcolor="rgba(0,0,0,0.1)",
                linecolor="rgba(0,0,0,0.2)",
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                showticklabels=False,
                gridcolor="rgba(0,0,0,0.1)",
                linecolor="rgba(0,0,0,0.2)",
                direction="clockwise",
                rotation=90
            ),
            domain=dict(
                x=[0.08, 0.92],
                y=[0.08, 0.92]
            )
        ),
        annotations=year_annotations,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.05,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=60, r=60, t=100, b=60),
        height=750,
        width=750,
        plot_bgcolor='white',
        paper_bgcolor='white',
        autosize=False
    )

    return fig
