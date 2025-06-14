import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def _create_empty_heatmap(message): 
    """Crée une heatmap vide avec un message d'erreur."""
    fig = go.Figure() 
    fig.add_annotation( text=message, x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False, font=dict(size=16, color="red") ) 
    fig.update_layout( title="Heatmap - Données non disponibles", height=400, xaxis=dict(visible=False), yaxis=dict(visible=False), plot_bgcolor='white' ) 
    return fig

def build_heatmap(df, events, selected_event, window_days=7): 
    """ Construit une heatmap montrant l'impact des événements géopolitiques sur les rendements boursiers autour de la date de l'événement.
    Parameters:
    -----------
    df : DataFrame avec colonnes [tickers] et index Date
    events : liste des événements avec name et date
    selected_event : nom de l'événement sélectionné
    window_days : nombre de jours de chaque côté de l'événement
    """

    # Trouver l'événement sélectionné
    event_info = None
    for event in events:
        if event['name'] == selected_event:
            event_info = event
            break

    if not event_info:
        return _create_empty_heatmap(f"Événement '{selected_event}' non trouvé")

    event_date = pd.to_datetime(event_info['date'])

    # === RÉCUPÉRER TOUS LES INDICES AVEC LEURS RENDEMENTS ===
    # Trouver toutes les colonnes de rendements
    return_columns = [col for col in df.columns if col.endswith('_return')]
    
    # Extraire les noms des indices (supprimer '_return')
    available_indices = [col.replace('_return', '') for col in return_columns]
    
    print(f"📊 Indices trouvés pour la heatmap: {len(available_indices)}")
    print(f"Liste: {available_indices}")
    
    if not available_indices:
        return _create_empty_heatmap("Aucune donnée de rendement disponible")


    # Créer la plage de jours autour de l'événement
    days_range = list(range(-window_days, window_days + 1))
    date_range = [event_date + pd.Timedelta(days=i) for i in days_range]

    # Convertir les données pour calculer les rendements
    df_returns = df.copy()


    # Construire les données pour la heatmap
    # Construire les données pour la heatmap (version avec gestion weekends)
    records = []
    for ticker in available_indices:
        return_col = f"{ticker}_return"
        if return_col not in df_returns.columns:
            continue
            
        for offset, date in zip(days_range, date_range):
            # Vérifier si c'est un weekend
            is_weekend = date.weekday() >= 5  # Samedi=5, Dimanche=6
            
            if date in df_returns.index:
                ret = df_returns.loc[date, return_col]
                if pd.notna(ret):
                    # CORRIGÉ: Convertir en pourcentage pour la cohérence
                    ret_percent = ret * 100
                    records.append({
                        "Indice": ticker,
                        "Jour": offset,
                        "Rendement": ret_percent,  # CORRIGÉ: valeur en %
                        "Date": date.strftime("%Y-%m-%d"),
                        "Text": f"{ret_percent:.1f}%"  # CORRIGÉ: affichage correct
                    })
                else:
                    # GARDER TEL QUEL: pour les valeurs N/A
                    records.append({
                        "Indice": ticker,
                        "Jour": offset,
                        "Rendement": np.nan,
                        "Date": date.strftime("%Y-%m-%d"),
                        "Text": "N/A"
                    })
            else:
                # Différencier weekends des vraies données manquantes
                if is_weekend:
                    # GARDER TEL QUEL: pour les weekends
                    records.append({
                        "Indice": ticker,
                        "Jour": offset,
                        "Rendement": np.nan,
                        "Date": date.strftime("%Y-%m-%d"),
                        "Text": "📅"  # Icône weekend
                    })
                else:
                    # GARDER TEL QUEL: pour les données manquantes
                    records.append({
                        "Indice": ticker,
                        "Jour": offset,
                        "Rendement": np.nan,
                        "Date": date.strftime("%Y-%m-%d"),
                        "Text": "❌"  # Vraie donnée manquante
                    })



    if not records:
        return _create_empty_heatmap("Aucune donnée de rendement disponible")

    # Créer le DataFrame pour la heatmap
    heatmap_df = pd.DataFrame(records)

    # Pivoter les données pour la heatmap
    z_matrix = heatmap_df.pivot(index="Indice", columns="Jour", values="Rendement")
    text_matrix = heatmap_df.pivot(index="Indice", columns="Jour", values="Text")
    date_matrix = heatmap_df.pivot(index="Indice", columns="Jour", values="Date")

    # Créer la heatmap
    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        z=z_matrix.values,
        x=z_matrix.columns,
        y=z_matrix.index,
        zmin=-15,  # Échelle adaptée aux rendements réels
        zmax=15,
        colorscale="RdYlGn",
        text=text_matrix.values,
        texttemplate="%{text}" if window_days <= 7 else "",  # Masquer si fenêtre > 7 jours
        textfont=dict(size=max(6, 12 - window_days)),  # Taille adaptative : 6-12px
        hovertemplate=(
            "<b>%{y}</b><br>" +
            "Jour: %{x}<br>" +
            "Rendement: %{z:.2f}%<br>" +
            "Date: %{customdata}<br>" +
            "📅 = Weekend (marchés fermés)<br>" +
            "<extra></extra>"
        ),
        customdata=date_matrix.values,
        colorbar=dict(
            title="Rendement (%)",
            len=0.7
        )
    ))

    # Configuration du layout
    fig.update_layout(
        title=dict(
            text=f"<b>Impact de '{selected_event}' sur les rendements boursiers</b><br><sub>Rendements journaliers autour de l'événement (±{window_days} jours)</sub>",
            x=0.5,
            font=dict(size=16, color="#2c3e50")
        ),
        xaxis=dict(
            title="Jours relatifs à l'événement",
            tickmode="linear",
            dtick=1,
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)"
        ),
        yaxis=dict(
            title="Indices boursiers",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)"
        ),
        height=500,
        margin=dict(l=100, r=80, t=100, b=60),
        plot_bgcolor='white',
        
        # Ligne verticale au jour 0 (événement)
        shapes=[
            dict(
                type="line",
                x0=0, x1=0,
                yref="paper", y0=0, y1=1,
                line=dict(color="black", width=2, dash="dash")
            )
        ],
        
        # Annotation pour le jour 0 
        annotations=[
            dict(
                x=-0.5, y=0.95,  # CORRIGÉ: Plus haut pour éviter le sous-titre
                xref="x", yref="paper",
                text="📅 Événement",  # CORRIGÉ: Texte plus court
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="black",
                font=dict(size=10, color="black"),  # CORRIGÉ: Police plus petite
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="black",
                borderwidth=1,
                borderpad=2  # AJOUTÉ: Espacement interne réduit
            )
        ]

    )
    return fig
