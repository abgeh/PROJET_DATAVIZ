import pandas as pd
import numpy as np
from data_loader import load_market_data
from data_processor import compute_daily_returns, compute_volatility

print("=== DEBUG COMPARAISON RENDEMENTS ===\n")
print("🔍 Comparaison entre Heatmap vs Choroplèthe")

# Charger les données comme dans l'app
df = load_market_data()
df = compute_daily_returns(df)
df = compute_volatility(df)

# Paramètres de test
event_name = "COVID-19"
event_date = pd.to_datetime("2020-03-11")
window_days = 7
post_window = 5  # Pour la choroplèthe

print(f"📅 Événement: {event_name} ({event_date.strftime('%Y-%m-%d')})")
print(f"📊 Fenêtre heatmap: ±{window_days} jours")
print(f"📊 Fenêtre choroplèthe: +{post_window} jours")

# === 1) REPRODUIRE LA LOGIQUE HEATMAP ===
print(f"\n🔥 === LOGIQUE HEATMAP ===")

# Récupérer les indices comme dans la heatmap
return_columns = [col for col in df.columns if col.endswith('_return')]
heatmap_indices = [col.replace('_return', '') for col in return_columns]

print(f"Indices heatmap: {len(heatmap_indices)}")
print(f"Échantillon: {heatmap_indices[:5]}")

# Plage de dates heatmap
days_range = list(range(-window_days, window_days + 1))
date_range = [event_date + pd.Timedelta(days=i) for i in days_range]

# Calculer les rendements heatmap pour quelques indices
heatmap_data = {}
for ticker in heatmap_indices[:3]:  # Analyser les 3 premiers
    return_col = f"{ticker}_return"
    heatmap_data[ticker] = {}
    
    print(f"\n--- {ticker} (Heatmap) ---")
    for offset, date in zip(days_range, date_range):
        if date in df.index and return_col in df.columns:
            ret = df.loc[date, return_col]
            if pd.notna(ret):
                heatmap_data[ticker][offset] = ret
                print(f"  Jour {offset:+2d} ({date.strftime('%m-%d')}): {ret:.4f}")
            else:
                print(f"  Jour {offset:+2d} ({date.strftime('%m-%d')}): N/A")
        else:
            print(f"  Jour {offset:+2d} ({date.strftime('%m-%d')}): DATE MANQUANTE")

# === 2) REPRODUIRE LA LOGIQUE CHOROPLÈTHE ===
print(f"\n🗺️ === LOGIQUE CHOROPLÈTHE ===")

# Configuration choroplèthe (comme dans l'app)
regions_map = {
    'Americas': ['^GSPC', '^DJI', '^IXIC'],
    'Europe': ['^FTSE', '^GDAXI', '^FCHI'],
    'Asia': ['^N225', '000001.SS', '^NSEI']
}

# Conversion en format long comme dans viz_choropleth
df_long = df.reset_index().melt(
    id_vars=['Date'], 
    var_name='Ticker', 
    value_name='Close'
).dropna()

# Filtrer seulement les colonnes de prix (pas _return)
df_long = df_long[~df_long['Ticker'].str.endswith(('_return', '_volatility'))]

# Trier et calculer les rendements comme dans la choroplèthe
df_long = df_long.sort_values(['Ticker', 'Date'])
df_long['ret'] = df_long.groupby('Ticker')['Close'].pct_change()

print(f"Données long format: {len(df_long)} lignes")
print(f"Tickers uniques: {df_long['Ticker'].nunique()}")

# Fenêtre post-événement pour choroplèthe
window = max(post_window, 5)
mask = (
    (df_long['Date'] >= event_date - pd.Timedelta(days=window)) &
    (df_long['Date'] <= event_date + pd.Timedelta(days=window))
)
df_win = df_long.loc[mask].copy()

print(f"Données dans la fenêtre: {len(df_win)} lignes")

# Calculer les rendements par région (comme dans choroplèthe)
choropleth_data = {}
for region, tickers in regions_map.items():
    sub = df_win[
        df_win['Ticker'].isin(tickers) & 
        (df_win['Date'] > event_date) & 
        (df_win['Date'] <= event_date + pd.Timedelta(days=post_window))
    ]
    
    if len(sub) > 0:
        mean_ret = sub['ret'].mean() * 100  # Conversion en %
        choropleth_data[region] = {
            'mean_return': mean_ret,
            'num_points': len(sub),
            'tickers': sub['Ticker'].unique().tolist()
        }
        
        print(f"\n--- {region} (Choroplèthe) ---")
        print(f"  Rendement moyen: {mean_ret:.4f}%")
        print(f"  Points de données: {len(sub)}")
        print(f"  Tickers: {sub['Ticker'].unique().tolist()}")
        
        # Détail des rendements individuels
        daily_rets = sub.groupby(['Date', 'Ticker'])['ret'].first().unstack(fill_value=np.nan)
        print(f"  Rendements quotidiens:")
        for date, row in daily_rets.iterrows():
            print(f"    {date.strftime('%m-%d')}: {dict(row.dropna())}")

# === 3) COMPARAISON DIRECTE ===
print(f"\n🔍 === COMPARAISON DIRECTE ===")

# Comparer les mêmes indices entre heatmap et choroplèthe
common_indices = set(heatmap_indices) & set([t for tickers in regions_map.values() for t in tickers])
print(f"Indices communs: {list(common_indices)}")

for ticker in list(common_indices)[:3]:
    print(f"\n--- Comparaison {ticker} ---")
    
    # Rendements heatmap (jour par jour)
    if ticker in heatmap_data:
        heatmap_rets = heatmap_data[ticker]
        print(f"  HEATMAP (rendements journaliers):")
        for day, ret in sorted(heatmap_rets.items()):
            if day >= 0:  # Seulement post-événement
                print(f"    Jour {day:+2d}: {ret:.4f}")
        
        # Moyenne des rendements post-événement dans la heatmap
        post_event_rets = [ret for day, ret in heatmap_rets.items() if 0 <= day <= post_window]
        if post_event_rets:
            heatmap_mean = np.mean(post_event_rets) * 100
            print(f"  HEATMAP Moyenne post-événement: {heatmap_mean:.4f}%")
    
    # Rendements choroplèthe (par région)
    for region, tickers in regions_map.items():
        if ticker in tickers and region in choropleth_data:
            choro_mean = choropleth_data[region]['mean_return']
            print(f"  CHOROPLÈTHE ({region}): {choro_mean:.4f}%")

# === 4) VÉRIFICATION DES CALCULS ===
print(f"\n🧮 === VÉRIFICATION DES CALCULS ===")

# Test sur un indice spécifique
test_ticker = '^GSPC'
if test_ticker in df.columns:
    print(f"Test sur {test_ticker}:")
    
    # Méthode 1: Rendement direct de la colonne _return
    return_col = f"{test_ticker}_return"
    if return_col in df.columns:
        day0_ret_method1 = df.loc[event_date, return_col] if event_date in df.index else None
        print(f"  Méthode 1 (_return): {day0_ret_method1:.6f}" if day0_ret_method1 is not None else "  Méthode 1: N/A")
    
    # Méthode 2: Calcul manuel pct_change()
    if event_date in df.index:
        event_idx = df.index.get_loc(event_date)
        if event_idx > 0:
            prev_date = df.index[event_idx - 1]
            current_price = df.loc[event_date, test_ticker]
            prev_price = df.loc[prev_date, test_ticker]
            if pd.notna(current_price) and pd.notna(prev_price) and prev_price != 0:
                manual_ret = (current_price - prev_price) / prev_price
                print(f"  Méthode 2 (manuel): {manual_ret:.6f}")
            else:
                print(f"  Méthode 2: Prix invalides")

# === 5) DIAGNOSTIC ===
print(f"\n💡 === DIAGNOSTIC ===")
print("Différences possibles entre heatmap et choroplèthe:")
print("1. 🔄 Calcul: Heatmap utilise colonnes _return, Choroplèthe recalcule")
print("2. 📅 Période: Heatmap jour par jour, Choroplèthe moyenne sur fenêtre")
print("3. 🌍 Agrégation: Choroplèthe moyenne par région")
print("4. 📊 Échelle: Heatmap affiche comme tel, Choroplèthe x100 pour %")

print(f"\n=== FIN DU DEBUG ===")
