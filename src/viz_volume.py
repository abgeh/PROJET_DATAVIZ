import numpy as np
import pandas as pd
import plotly.graph_objects as go

def build_polar_volume_chart(
    df: pd.DataFrame,
    events: list[dict],
    ticker: str,
    rolling_window: int = 7,
    start_date: str = "2008-01-01",
    end_date: str = "2023-12-31"
) -> go.Figure:
    """
    Diagramme polaire du volume lissé sur rolling_window jours,
    avec repères d'événements.
    """

    # 0) Clamp de rolling_window pour qu'il soit au moins 1
    try:
        rw = int(rolling_window)
    except (TypeError, ValueError):
        rw = 1
    if rw < 1:
        rw = 1

    # 1) Préparation du cadre temporel
    full_start = pd.to_datetime(start_date)
    full_end   = pd.to_datetime(end_date)
    total_days = (full_end - full_start).days

    # 2) Filtrer / trier / lisser
    dft = (
        df[df["Ticker"] == ticker]
        .copy()
        .assign(Date=lambda d: pd.to_datetime(d["Date"]))
        .sort_values("Date")
    )
    dft["vol_smooth"] = dft["Volume"].rolling(rw, min_periods=1).mean()
    dft["Theta"]      = 360 * (dft["Date"] - full_start).dt.days / total_days
    dft["Radius"]     = dft["vol_smooth"] / 1e9  # milliards

    max_r = dft["Radius"].max() or 1

    fig = go.Figure()

    # 3) Trace principale + hover date/volume
    fig.add_trace(go.Scatterpolar(
        theta       = dft["Theta"],
        r           = dft["Radius"],
        mode        = "lines",
        line        = dict(color="teal", width=1),
        fill        = "toself",
        fillcolor   = "rgba(0,128,128,0.2)",
        customdata  = np.stack([
                          dft["Date"].dt.strftime("%Y-%m-%d"),
                          dft["Radius"]
                        ], axis=1),
        hovertemplate=
            "Date : %{customdata[0]}<br>"
            "Volume glissant : %{customdata[1]:.2f} Md<extra></extra>",
        showlegend=False
    ))

    # 4) Repères annuels
    for year in range(full_start.year, full_end.year + 1):
        anchor = pd.Timestamp(f"{year}-01-01")
        angle  = 360 * (anchor - full_start).days / total_days
        fig.add_trace(go.Scatterpolar(
            theta=[angle],
            r    =[max_r * 1.03],
            mode ="text",
            text =[str(year)],
            textfont=dict(size=9, color="black"),
            hoverinfo="skip",
            showlegend=False
        ))

    # 5) Événements géopolitiques (ligne + label jitter)
    for idx, ev in enumerate(events):
        ev_date    = pd.to_datetime(ev["date"])
        base_angle = 360 * (ev_date - full_start).days / total_days

        # Ligne de repère
        fig.add_trace(go.Scatterpolar(
            theta      = [base_angle, base_angle],
            r          = [0, max_r],
            mode       = "lines",
            line       = dict(dash="dash", color="brown", width=1),
            hoverinfo  = "skip",
            showlegend = False
        ))

        # Label légèrement décalé pour éviter chevauchement
        angle_jit = base_angle + ((idx % 2) * 4 - 2)   # ±2°
        r_label   = max_r * (1.08 + (idx % 2) * 0.03)
        fig.add_trace(go.Scatterpolar(
            theta      = [angle_jit],
            r          = [r_label],
            mode       = "text",
            text       = [ev["name"]],
            textfont   = dict(size=8, color="brown"),
            hoverinfo  = "skip",
            showlegend = False
        ))

    # 6) Mise en page
    fig.update_layout(
        title = f"Volume {ticker} (2008–2023) – {rw}-j glissant",
        polar = dict(radialaxis=dict(visible=False), angularaxis=dict(visible=False)),
        margin=dict(t=50,b=20,l=20,r=20)
    )

    return fig
