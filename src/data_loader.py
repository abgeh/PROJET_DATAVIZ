import pandas as pd
from pathlib import Path
import glob

def load_market_data(data_dir="data", pattern="*_Glob*l_Markets_Data.csv"):
    """
    Charge et combine tous les fichiers CSV de données de marché.
    Retourne un DataFrame avec les dates en index et les tickers en colonnes.
    
    Pattern modifié pour capturer les fichiers avec "Global" et "Globla" (faute de frappe)
    """
    data_path = Path(data_dir)
    
    # Trouver tous les fichiers CSV correspondant au pattern élargi
    csv_files = glob.glob(str(data_path / pattern))
    
    if not csv_files:
        raise FileNotFoundError(f"Aucun fichier trouvé avec le pattern {pattern} dans {data_dir}")

    
    # Lire et combiner tous les fichiers
    all_dataframes = []
    
    for file in csv_files:

        df = pd.read_csv(file)
        
        # Vérifier que les colonnes nécessaires existent
        required_cols = ['Ticker', 'Date', 'Volume']
        if not all(col in df.columns for col in required_cols):
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
    
    
    pivoted_df = combined_df.pivot_table(
        index='Date', 
        columns='Ticker', 
        values='Volume', 
        aggfunc='first'
    )
    
    # Trier par date
    pivoted_df = pivoted_df.sort_index()
    
    
    return pivoted_df
