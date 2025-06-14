import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import pycountry_convert as pc
import numpy as np

def build_choropleth(df, events, event_name, region_map, post_window=5, range_color=[-100, 100]):
    """
    Construit une carte choroplèthe montrant l'impact des événements géopolitiques 
    sur les rendements boursiers par région.
    Utilise la logique adaptée du code de travail fourni.
    """
    
    # === 1) TROUVER L'ÉVÉNEMENT SÉLECTIONNÉ ===
    selected_event = None
    for event in events:
        if event['name'] == event_name:
            selected_event = event
            break
    
    if not selected_event:
        return _create_empty_choropleth(f"Événement '{event_name}' non trouvé")
    
    event_date = pd.to_datetime(selected_event['date'])
    
    # === 2) PRÉPARER LES DONNÉES AVEC RENDEMENTS ===
    # Convertir le df pivot en format long pour les calculs de rendements
    df_long = df.reset_index().melt(
        id_vars=['Date'], 
        var_name='Ticker', 
        value_name='Close'
    ).dropna()
    
    # Trier et calculer les rendements journaliers
    df_long = df_long.sort_values(['Ticker', 'Date'])
    df_long['ret'] = df_long.groupby('Ticker')['Close'].pct_change()
    
    # === 3) DÉFINIR LA FENÊTRE AUTOUR DE L'ÉVÉNEMENT ===
    window = max(post_window, 5)  # Au moins 5 jours pour avoir des données
    mask = (
        (df_long['Date'] >= event_date - pd.Timedelta(days=window)) &
        (df_long['Date'] <= event_date + pd.Timedelta(days=window))
    )
    df_win = df_long.loc[mask].copy()
    
    if len(df_win) == 0:
        return _create_empty_choropleth(f"Pas de données pour la période autour du {event_date.strftime('%Y-%m-%d')}")
    
    # === 4) CALCUL DES RENDEMENTS MOYENS POST-ÉVÉNEMENT PAR RÉGION ===
    regions = []
    for region, tickers in region_map.items():
        # Filtrer les données pour cette région et période post-événement
        sub = df_win[
            df_win['Ticker'].isin(tickers) & 
            (df_win['Date'] > event_date) & 
            (df_win['Date'] <= event_date + pd.Timedelta(days=post_window))
        ]
        
        if len(sub) > 0:
            mean_ret = sub['ret'].mean() * 100  # Convertir en pourcentage
            num_indices = len(sub['Ticker'].unique())
            indices_list = ', '.join(sorted(sub['Ticker'].unique()))
        else:
            mean_ret = 0
            num_indices = 0
            indices_list = "Aucun indice disponible"
        
        regions.append({
            'region': region, 
            'mean_return': mean_ret,
            'num_indices': num_indices,
            'indices': indices_list
        })
    
    region_df = pd.DataFrame(regions)
    
    if len(region_df) == 0:
        return _create_empty_choropleth("Aucune donnée de rendement calculée")
    
    # === 5) CONSTRUIRE LA CARTE ISO DYNAMIQUE ===
    continent_codes_map = {
        'Americas': ['NA', 'SA'],  # Amérique du Nord + Sud
        'Europe': ['EU'],
        'Asia': ['AS', 'OC']       # Asie + Océanie (pour inclure Australie)
    }
    
    iso_map = {}
    for region, cont_codes in continent_codes_map.items():
        isos = []
        for country in pycountry.countries:
            try:
                cc2 = country.alpha_2
                cont = pc.country_alpha2_to_continent_code(cc2)
                if cont in cont_codes:
                    isos.append(country.alpha_3)
            except Exception:
                continue
        iso_map[region] = isos
    
    # === 6) EXPLOSER REGION_DF POUR AVOIR UN ENREGISTREMENT PAR PAYS ISO ===
    rows = []
    for _, row in region_df.iterrows():
        region_name = row['region']
        if region_name in iso_map:
            for iso in iso_map[region_name]:
                rows.append({
                    'iso_alpha': iso,
                    'region': region_name,
                    'mean_return': row['mean_return'],
                    'num_indices': row['num_indices'],
                    'indices': row['indices']
                })
    
    if not rows:
        return _create_empty_choropleth("Erreur dans le mapping des pays")
    
    map_df = pd.DataFrame(rows)
    
    # === 7) CRÉER LA CARTE CHOROPLÈTHE AVEC ÉCHELLE PERSONNALISÉE ===
    # Zone neutre : -1% à +1% en jaune
    custom_colorscale = [
        [0.0, '#800000'],   # -100% : 
        [0.40, '#B22222'],   # -20% : 
        [0.45, '#FF0800'],   # -10% : 
        [0.475, '#FF7F50'],   # -5% : 

        [0.495, '#FFF3CD'], # -0.5% : Jaune clair
        [0.5, '#FFEB3B'],   # 0% : Jaune vif (neutre)
        [0.505, '#FFF3CD'], # +0.5% : Jaune clair

        [0.525, '#81C784'], # +5%
        [0.55, '#4CAF50'], # +10% : 
        [0.60, '#00A86B'],    # +20% : 
        [1.0, '#1B5E20']    # +100% : Vert très foncé (boom)
    ]

    fig = px.choropleth(
        map_df,
        locations='iso_alpha',
        color='mean_return',
        hover_name='region',
        color_continuous_scale=custom_colorscale,  # CHANGÉ: Utiliser l'échelle personnalisée
        range_color=range_color,
        color_continuous_midpoint=0,
        title=f"Impact de '{event_name}' sur les marchés mondiaux<br><sub>Rendement moyen {post_window} jours après le {event_date.strftime('%d/%m/%Y')}</sub>"
    )
    
    # === 8) PERSONNALISER LE HOVER ===
    fig.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>" +
            "Rendement: %{z:.2f}%<br>" +
            "Indices: %{customdata[0]}<br>" +
            "Nombre d'indices: %{customdata[1]}<br>" +
            f"Période: {post_window} jours après {event_date.strftime('%d/%m/%Y')}<br>" +
            "<extra></extra>"
        ),
        customdata=map_df[['indices', 'num_indices']].values
    )
    
    # === 9) MISE À JOUR DU LAYOUT ===
    fig.update_layout(
        geo=dict(
            showframe=False, 
            showcoastlines=True,
            projection_type='equirectangular'
        ),
        title=dict(
            x=0.5,
            font=dict(size=16, color="#2c3e50"),
            pad=dict(t=20)
        ),
        coloraxis_colorbar=dict(
        title="Rendement (%)",
        tickformat=".0f",
        len=0.8,
        thickness=20,
        # CHANGÉ: Points clés pour l'échelle personnalisée
        tickvals=[-100, -20, 0, 20, 100],
        ticktext=["-100%", "-20%", "0%", "+20%", "+100%"],
        tickfont=dict(size=11),
        x=1.02
        ),

        height=600,
        margin=dict(l=0, r=0, t=80, b=20)
    )
    
    return fig


def _create_empty_choropleth(message): 
    """Crée une carte vide avec un message d'erreur."""
    fig = go.Figure() 
    fig.add_annotation( text=message, x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False, font=dict(size=16, color="red") ) 
    fig.update_layout( title="Carte choroplèthe - Données non disponibles", height=400, xaxis=dict(visible=False), yaxis=dict(visible=False) ) 
    return fig
