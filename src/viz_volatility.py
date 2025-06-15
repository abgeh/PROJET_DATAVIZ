import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def build_volatility_chart(df, events, selected_event, window_days=7, rolling_window=5, grouping="individual"): 
    """ Construit un graphique de volatilité montrant l'évolution de l'écart-type des rendements autour d'un événement géopolitique.
    Parameters:
    -----------
    df : DataFrame avec colonnes [tickers] et index Date
    events : liste des événements avec name et date
    selected_event : nom de l'événement sélectionné
    window_days : nombre de jours de chaque côté de l'événement
    rolling_window : fenêtre mobile pour calculer la volatilité
    grouping : "individual", "region", ou "type" (Actions vs Matières premières)
    """

    # Trouver l'événement sélectionné
    event_info = None
    for event in events:
        if event['name'] == selected_event:
            event_info = event
            break

    if not event_info:
        return _create_empty_volatility(f"Événement '{selected_event}' non trouvé")

    event_date = pd.to_datetime(event_info['date'])

    # === FORCER LE CALCUL DE VOLATILITÉ POUR TOUS LES INDICES ===
    # Au lieu d'utiliser les colonnes existantes, recalculer pour s'assurer d'avoir tout
    df_calc = _calculate_volatility(df, rolling_window)
    
    # Convertir en format long pour le traitement
    df_long = df_calc.reset_index().melt(
        id_vars=['Date'], 
        var_name='Column', 
        value_name='Value'
    ).dropna()

    # Séparer les colonnes de volatilité
    df_volatility = df_long[df_long['Column'].str.endswith('_volatility')].copy()
    df_volatility['Ticker'] = df_volatility['Column'].str.replace('_volatility', '')
    df_volatility = df_volatility.rename(columns={'Value': 'volatility'})

    # DEBUG: Afficher les indices trouvés
    unique_tickers = df_volatility['Ticker'].unique()
    print(f"📊 Indices volatilité trouvés: {len(unique_tickers)}")
    print(f"Liste: {list(unique_tickers)}")

    if len(df_volatility) == 0:
        return _create_empty_volatility("Aucune donnée de volatilité disponible")


    # Filtrer autour de l'événement
    mask = (
        (df_volatility['Date'] >= event_date - pd.Timedelta(days=window_days)) &
        (df_volatility['Date'] <= event_date + pd.Timedelta(days=window_days))
    )
    df_win = df_volatility.loc[mask].copy()

    if len(df_win) == 0:
        return _create_empty_volatility(f"Aucune donnée autour du {event_date.strftime('%Y-%m-%d')}")

    # Calculer les jours relatifs
    df_win['day_rel'] = (df_win['Date'] - event_date).dt.days

    # Appliquer le groupement
    df_grouped = _apply_grouping(df_win, grouping)

    # Créer le graphique
    fig = px.line(
        df_grouped,
        x='day_rel',
        y='volatility',
        color='Group',
        labels={
            'day_rel': 'Jours relatifs à l\'événement',
            'volatility': f'Volatilité (σ {rolling_window} jours)',
            'Group': 'Indice/Groupe'
        },
        title=f"Évolution de la volatilité autour de '{selected_event}'<br><sub>Fenêtre d'analyse: ±{window_days} jours, Volatilité: écart-type mobile {rolling_window} jours</sub>"
    )

    # Personnaliser l'apparence
    fig.update_layout(
        xaxis=dict(
            title="Jours relatifs à l'événement",
            tickmode='linear',
            tick0=-window_days,
            dtick=max(1, window_days // 5),  # Adapter l'espacement selon la fenêtre
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)"
        ),
        yaxis=dict(
            title=f"Volatilité (σ {rolling_window} jours)",  
            tickformat='.3f',
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)"
        ),

        legend=dict(
            title='',
            orientation='h',  # CHANGÉ: Toujours horizontale (supprimé la condition)
            yanchor='bottom',
            y=0.98,
            xanchor='left',
            x=0
        ),
        template='plotly_white',
        height=500,
        margin=dict(l=60, r=20, t=160, b=80),  


        
        # Ligne verticale au jour 0 (événement)
        shapes=[
            dict(
                type="line",
                x0=0, x1=0,
                yref="paper", y0=0, y1=1,
                line=dict(color="red", width=2, dash="dash"),
                opacity=0.7
            )
        ],
        
        # Annotation pour le jour 0
        annotations=[
            dict(
                x=-0.3, y=0.01,  # CHANGÉ: Flèche en bas du graphique
                xref="x", yref="paper",
                text="📅 Événement",
                showarrow=True,
                arrowhead=2,
                arrowsize=1.2,
                arrowwidth=2,
                arrowcolor="red",
                ay=25,  # AJOUTÉ: Flèche pointant vers le haut
                font=dict(size=9, color="red"),
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="red",
                borderwidth=1
            )
        ]
    )

    # Améliorer le hover
    fig.update_traces(
        hovertemplate=(
            "<b>%{fullData.name}</b><br>" +
            "Jour: %{x}<br>" +
            "Volatilité: %{y:.4f}<br>" +
            "Date: %{customdata}<br>" +
            "<extra></extra>"
        )
    )

    return fig

def _calculate_volatility(df, rolling_window):
    """Calcule la volatilité pour tous les indices disponibles."""
    df_calc = df.copy()
    
    # Récupérer tous les indices (colonnes qui ne sont pas des calculs)
    base_columns = [col for col in df.columns if not col.endswith(('_return', '_volatility'))]
    
    print(f"🔍 Calcul volatilité pour {len(base_columns)} indices")
    
    for col in base_columns:
        try:
            # Utiliser la colonne _return si elle existe, sinon calculer
            return_col = f"{col}_return"
            if return_col in df.columns:
                returns = df[return_col]
            else:
                returns = df[col].pct_change()
            
            # Calculer la volatilité (écart-type mobile)
            volatility = returns.rolling(window=rolling_window, min_periods=1).std()
            df_calc[f"{col}_volatility"] = volatility
            
        except Exception as e:
            print(f"⚠️ Erreur calcul volatilité pour {col}: {e}")
            continue
    
    return df_calc


def _apply_grouping(df_win, grouping): 
    """Applique le groupement spécifié."""
    if grouping == "individual": # Chaque indice séparément 
        df_grouped = df_win.copy() 
        df_grouped['Group'] = df_grouped['Ticker']

    elif grouping == "region":
        # CHANGÉ: Seulement 3 régions principales
        region_map = {
            'Americas': ['^GSPC', '^DJI', '^IXIC', '^MXX'],
            'Europe': ['^FTSE', '^GDAXI', '^FCHI', '^IBEX'],
            'Asia': ['^N225', '000001.SS', '^HSI', '^NSEI', '^AXJO', '^BSESN']
        }
        
        def get_region(ticker):
            for region, tickers in region_map.items():
                if ticker in tickers:
                    return region
            # CHANGÉ: Ignorer les autres au lieu de créer une catégorie "Other"
            return None
        
        df_win['Region'] = df_win['Ticker'].apply(get_region)
        # CHANGÉ: Filtrer pour garder seulement les 3 régions principales
        df_win = df_win[df_win['Region'].notna()].copy()
        
        # Moyenne par région et par jour
        df_grouped = df_win.groupby(['day_rel', 'Date', 'Region'])['volatility'].mean().reset_index()
        df_grouped['Group'] = df_grouped['Region']

    
    elif grouping == "type":
        # Actions vs Matières premières
        commodities = ['CL=F', 'GC=F']
        df_win['Type'] = df_win['Ticker'].apply(lambda x: 'Matières premières' if x in commodities else 'Actions')
        # Moyenne par type et par jour
        df_grouped = df_win.groupby(['day_rel', 'Date', 'Type'])['volatility'].mean().reset_index()
        df_grouped['Group'] = df_grouped['Type']

    else:
        df_grouped = df_win.copy()
        df_grouped['Group'] = df_grouped['Ticker']

    return df_grouped

def _create_empty_volatility(message): 
    """Crée un graphique vide avec un message d'erreur."""
    fig = go.Figure() 
    fig.add_annotation( text=message, x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False, font=dict(size=16, color="red") ) 
    fig.update_layout( title="Volatilité - Données non disponibles", height=400, xaxis=dict(visible=False), yaxis=dict(visible=False), plot_bgcolor='white' ) 
    return fig
