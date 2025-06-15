import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def build_compare_chart(df, events, mode="return", selected_category="Géopolitique"):
    """
    Crée un graphique en barres comparant les rendements ou volatilités moyens
    par type d’actif pour une catégorie d’événement donnée.
    """

    # Vérification des champs requis
    if mode not in ["return", "volatility"]:
        raise ValueError("Le mode doit être 'return' ou 'volatility'")

    # Liste des colonnes de rendement ou volatilité
    suffix = "_return" if mode == "return" else "_volatility"
    columns = [col for col in df.columns if col.endswith(suffix)]

    if not columns:
        return go.Figure().add_annotation(
            text="Données indisponibles", showarrow=False
        )

    # Catégories d'événements disponibles
    filtered_events = [e for e in events if e["category"] == selected_category]

    if not filtered_events:
        return go.Figure().add_annotation(
            text=f"Aucun événement trouvé pour la catégorie '{selected_category}'", showarrow=False
        )

    # Plage autour des événements
    window = 5
    records = []

    for event in filtered_events:
        ev_date = pd.to_datetime(event["date"])
        date_range = pd.date_range(ev_date - pd.Timedelta(days=window), ev_date + pd.Timedelta(days=window))

        subset = df.loc[df.index.isin(date_range)]

        for col in columns:
            asset = col.replace(suffix, "")
            values = subset[col].dropna()
            if len(values) > 0:
                avg = values.mean() * (100 if mode == "return" else 1)
                records.append({
                    "Actif": asset,
                    "Valeur": avg,
                    "Type": event["category"],
                    "Nom événement": event["name"]
                })

    if not records:
        return go.Figure().add_annotation(text="Aucune donnée calculée", showarrow=False)

    final_df = pd.DataFrame(records)
    final_df.sort_values("Valeur", ascending=False, inplace=True)

    fig = px.bar(
        final_df,
        x="Actif",
        y="Valeur",
        color="Nom événement",
        barmode="group",
        labels={"Valeur": "Rendement moyen (%)" if mode == "return" else "Volatilité"},
        title=f"<b>{'Rendements' if mode=='return' else 'Volatilité'} moyens par actif</b><br><sub>Catégorie : {selected_category}</sub>"
    )

    fig.update_layout(
        height=500,
        plot_bgcolor="white",
        xaxis_title="Type d’actif",
        yaxis_title="Rendement (%)" if mode == "return" else "Volatilité",
        margin=dict(l=40, r=40, t=80, b=40),
        legend_title="Événement"
    )
    return fig
