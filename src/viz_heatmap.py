import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


data_dir = os.path.join("src", "data")
csv_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".csv")]
df_list = []

for file in csv_files:
    df = pd.read_csv(file)
    df["Year"] = int(os.path.basename(file)[:4])
    df_list.append(df)

df = pd.concat(df_list, ignore_index=True)
df["Date"] = pd.to_datetime(df["Date"])
df.sort_values("Date", inplace=True)


events = {
    "COVID-19 (2020-03-16)": pd.Timestamp("2020-03-16"),
    "Crise Ukraine (2022-02-24)": pd.Timestamp("2022-02-24"),
    "Élection Trump (2016-11-08)": pd.Timestamp("2016-11-08")
}


buttons = []
fig = go.Figure()

for i, (label, event_date) in enumerate(events.items()):
    indices = ["^GSPC", "^FTSE", "^DJI", "^IXIC", "^N225", "^N100", "000001.SS"]
    days_range = list(range(-7, 8))
    date_range = [event_date + pd.Timedelta(days=i) for i in days_range]

    records = []
    for ticker in indices:
        ticker_data = df[df["Ticker"] == ticker].copy()
        ticker_data.set_index("Date", inplace=True)
        ticker_data.sort_index(inplace=True)
        ticker_data["Return"] = ticker_data["Close"].pct_change() * 100

        for offset, date in zip(days_range, date_range):
            ret = ticker_data.loc[date, "Return"] if date in ticker_data.index else np.nan
            records.append({
                "Indice": ticker,
                "Jour": offset,
                "Rendement": ret,
                "Date": date.strftime("%Y-%m-%d"),
                "Text": f"{ret:.1f}" if not np.isnan(ret) else ""
            })

    heatmap_df = pd.DataFrame(records)
    z = heatmap_df.pivot(index="Indice", columns="Jour", values="Rendement").to_numpy()
    customdata = heatmap_df.pivot(index="Indice", columns="Jour", values="Date").to_numpy()
    text = heatmap_df.pivot(index="Indice", columns="Jour", values="Text").to_numpy()

    fig.add_trace(go.Heatmap(
        z=z,
        x=days_range,
        y=indices,
        visible=(i == 0),
        zmin=-10,
        zmax=5,
        colorscale="RdYlGn",
        text=text,
        texttemplate="%{text}",
        hovertemplate="Date: %{customdata}<br>Jour: %{x}<br>Indice: %{y}<br>Rendement: %{z:.2f}%<extra></extra>",
        customdata=customdata,
        colorbar=dict(title="Rendement journalier (%)") if i == 0 else None
    ))

    visibility = [j == i for j in range(len(events))]
    buttons.append(dict(label=label, method="update", args=[{"visible": visibility}]))


fig.update_layout(
    shapes=[dict(
        type="line",
        x0=0, x1=0,
        yref="paper", y0=0, y1=1,
        line=dict(color="black", dash="dash")
    )],
    updatemenus=[dict(
        type="dropdown",
        direction="down",
        buttons=buttons,
        showactive=True,
        x=1.15,
        y=1.15
    )],
    title="<b>Impact des événements géopolitiques sur les rendements boursiers</b><br>Sélectionne un événement dans le menu déroulant",
    xaxis_title="Jours autour de l'événement (Jour 0)",
    yaxis_title="Indice",
    height=500,
    margin=dict(l=40, r=40, t=80, b=40)
)

fig.show()