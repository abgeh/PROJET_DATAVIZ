import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def build_compare_chart(df, events, selected_category="Geopolitique", window_days=0, mode="return"): 
    """ Construit un diagramme à barres groupees comparant l'impact des evenements par categorie et type d'actif (indices boursiers vs matières premières).
    Parameters:
    -----------
    df : DataFrame avec colonnes [tickers] et index Date
    events : liste des evenements avec name, date et category
    selected_category : categorie d'evenement à analyser
    window_days : fenêtre temporelle (0 = jour J seulement)
    mode : "return" ou "volatility"
    """
    # Classification des actifs
    commodities = ['CL=F', 'GC=F']  # Matières premières (petrole, or)

    # Filtrer les evenements par categorie
    filtered_events = [e for e in events if e.get("category") == selected_category]

    if not filtered_events:
        return _create_empty_compare(f"Aucun evenement trouve pour la categorie '{selected_category}'")

    records = []

    for event in filtered_events:
        event_date = pd.to_datetime(event["date"])
        event_name = event["name"]
        
        # Definir la fenêtre d'analyse
        if window_days == 0:
            # Seulement le jour de l'evenement
            analysis_dates = [event_date] if event_date in df.index else []
        else:
            # Fenêtre autour de l'evenement
            start_date = event_date - pd.Timedelta(days=window_days)
            end_date = event_date + pd.Timedelta(days=window_days)
            analysis_dates = [d for d in pd.date_range(start_date, end_date) if d in df.index]
        
        if not analysis_dates:
            continue
        
        # Recalculer la volatilité pour la fenêtre spécifiée
        if mode == "volatility":
            # Recalculer la volatilité sur la fenêtre d'analyse pour cet événement
            volatility_window = max(3, len(analysis_dates))  # Fenêtre adaptative
            df_temp = df.copy()
            
            # Recalculer la volatilité avec la nouvelle fenêtre
            for col in df.columns:
                if not col.endswith(('_return', '_volatility')):
                    return_col = f"{col}_return"
                    if return_col in df.columns:
                        vol_series = df[return_col].rolling(window=volatility_window, min_periods=1).std()
                        df_temp[f"{col}_volatility"] = vol_series
            
            df_working = df_temp
            suffix = "_volatility"
        else:
            df_working = df
            suffix = "_return"

        
        # Indices boursiers
        indices_values = []
        # Matières premières
        commodities_values = []
        
        for col in df.columns:
            if col.endswith(suffix):
                ticker = col.replace(suffix, "")
                
                # Recuperer les valeurs pour les dates d'analyse
                event_values = df_working.loc[analysis_dates, col].dropna()
                
                if len(event_values) > 0:
                    avg_value = event_values.mean()
                    
                    if mode == "return":
                        # Les colonnes _return sont TOUJOURS en décimal, convertir en %
                        avg_value *= 100
                        # Plafonner à des valeurs raisonnables
                        avg_value = max(-50, min(50, avg_value))
                    else:
                        # Les colonnes _volatility sont en décimal, convertir en %
                        avg_value *= 100
                        # La volatilité ne peut pas être négative et on plafonne à 20%
                        avg_value = max(0, min(20, avg_value))

                    
                    # Classer par type d'actif
                    if ticker in commodities:
                        commodities_values.append(avg_value)
                    else:
                        indices_values.append(avg_value)
        
        # Calculer les moyennes par type d'actif
        if indices_values:
            indices_avg = np.mean(indices_values)
            records.append({
                "evenement": event_name,
                "Type d'actif": "Indices boursiers",
                "Valeur": indices_avg,
                "Date": event_date.strftime("%Y-%m-%d"),
                "Categorie": selected_category,
                "Nombre d'actifs": len(indices_values)
            })
        
        if commodities_values:
            commodities_avg = np.mean(commodities_values)
            records.append({
                "evenement": event_name,
                "Type d'actif": "Matières premières",
                "Valeur": commodities_avg,
                "Date": event_date.strftime("%Y-%m-%d"),
                "Categorie": selected_category,
                "Nombre d'actifs": len(commodities_values)
            })

    if not records:
        return _create_empty_compare(f"Aucune donnee disponible pour '{selected_category}'")

    # Creer le DataFrame
    df_viz = pd.DataFrame(records)

    # Creer le graphique à barres groupees
    fig = px.bar(
        df_viz,
        x="evenement",
        y="Valeur",
        color="Type d'actif",
        barmode="group",
        color_discrete_map={
            "Indices boursiers": "#2E86AB",
            "Matières premières": "#A23B72"
        },
        labels={
            "Valeur": f"{'Rendement' if mode=='return' else 'Volatilite'} (%)",
            "evenement": "evenements majeurs",
            "Type d'actif": "Type d'actif"
        }
    )

    # Titre dynamique
    window_text = "Jour J" if window_days == 0 else f"±{window_days} jours"
    metric_text = "Rendements moyens" if mode == "return" else "Volatilite moyenne"

    fig.update_layout(
        title=dict(
            text=f"<b>{metric_text} par type d'actif</b><br><sub>Categorie : {selected_category} • Fenêtre : {window_text}</sub>",
            x=0.5,
            font=dict(size=16, color="#2c3e50")
        ),
        xaxis=dict(
            title="evenements majeurs",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)"
        ),
        yaxis=dict(
            title=f"{'Rendement' if mode=='return' else 'Volatilite'} (%)",
            tickformat='.2f',
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            zeroline=True,
            zerolinecolor="rgba(0,0,0,0.3)",
            zerolinewidth=1
        ),
        legend=dict(
            title="",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        template='plotly_white',
        height=500,
        margin=dict(l=60, r=60, t=120, b=80),
        plot_bgcolor='white'
    )

    # hover
    fig.update_traces(
        hovertemplate=(
            "<b>%{fullData.name}</b><br>" +
            "evenement: %{x}<br>" +
            f"{'Rendement' if mode=='return' else 'Volatilite'}: %{{y:.2f}}%<br>" +
            "Date: %{customdata[0]}<br>" +
            "Actifs analyses: %{customdata[1]}<br>" +
            "<extra></extra>"
        ),
        customdata=df_viz[["Date", "Nombre d'actifs"]].values
    )

    return fig

def _create_empty_compare(message): 
    """Cree un graphique vide avec un message d'erreur."""
    fig = go.Figure() 
    fig.add_annotation( text=message, x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False, font=dict(size=16, color="red") ) 
    fig.update_layout( title="Comparaison par categorie - Donnees non disponibles", height=400, xaxis=dict(visible=False), yaxis=dict(visible=False), plot_bgcolor='white' ) 
    return fig