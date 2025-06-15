import pandas as pd
from pathlib import Path
import glob

def load_market_data(data_dir="src/data", pattern="20*_Global_Markets_Data.csv"):
    """
    Charge et combine tous les fichiers CSV de données de marché.
    Retourne un DataFrame avec les dates en index et les tickers en colonnes.
    """
    data_path = Path(data_dir)
    
    # Trouver tous les fichiers CSV correspondant au pattern
    csv_files = glob.glob(str(data_path / pattern))
    
    if not csv_files:
        raise FileNotFoundError(f"Aucun fichier trouvé avec le pattern {pattern} dans {data_dir}")
    
    print(f"Chargement de {len(csv_files)} fichiers CSV...")
    
    # Lire et combiner tous les fichiers
    all_dataframes = []
    
    for file in csv_files:
        print(f"  - Lecture de {Path(file).name}")
        df = pd.read_csv(file)
        
        # Vérifier que les colonnes nécessaires existent
        required_cols = ['Ticker', 'Date', 'Volume']
        if not all(col in df.columns for col in required_cols):
            print(f"    ⚠️  Colonnes manquantes dans {file}: {df.columns.tolist()}")
            continue
            
        # Garder seulement les colonnes nécessaires
        df = df[['Ticker', 'Date', 'Volume']].copy()
        all_dataframes.append(df)
    
    if not all_dataframes:
        raise ValueError("Aucun fichier valide trouvé")
    
    # Combiner tous les DataFrames
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    
    # Convertir la colonne Date
    combined_df['Date'] = pd.to_datetime(combined_df['Date'])
    
    # Nettoyer les données (supprimer les valeurs nulles/négatives)
    combined_df = combined_df.dropna(subset=['Volume'])
    combined_df = combined_df[combined_df['Volume'] >= 0]
    
    print(f"Données combinées: {len(combined_df)} lignes")
    print(f"Tickers uniques: {combined_df['Ticker'].nunique()}")
    print(f"Période: {combined_df['Date'].min()} à {combined_df['Date'].max()}")
    
    # PIVOT: Transformer de format long vers format wide
    # Date en index, Ticker en colonnes, Volume en valeurs
    pivoted_df = combined_df.pivot_table(
        index='Date', 
        columns='Ticker', 
        values='Volume', 
        aggfunc='first'  # Si doublons, prendre la première valeur
    )
    
    # Trier par date
    pivoted_df = pivoted_df.sort_index()
    
    # Afficher les tickers disponibles
    available_tickers = pivoted_df.columns.tolist()
    print(f"\nTickers disponibles après pivot: {len(available_tickers)}")
    print(f"Liste: {available_tickers}")
    
    return pivoted_df
