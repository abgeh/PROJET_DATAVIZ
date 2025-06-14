import pandas as pd
import numpy as np

def compute_daily_returns(df):
    """
    Calcule les rendements journaliers sur les volumes.
    df: DataFrame avec dates en index, tickers en colonnes, volumes en valeurs
    """
    # Calculer les variations journalières de volume (en pourcentage)
    returns_df = df.pct_change().fillna(0)
    
    # Ajouter un préfixe pour distinguer les colonnes de rendement
    returns_df = returns_df.add_suffix('_return')
    
    # Combiner les données originales avec les rendements
    result = pd.concat([df, returns_df], axis=1)
    
    return result

def compute_volatility(df, window=30):
    """
    Calcule la volatilité glissante sur les volumes.
    df: DataFrame avec dates en index, tickers en colonnes
    window: fenêtre glissante pour la volatilité
    """
    # Identifier les colonnes de volume (sans suffixe _return)
    volume_cols = [col for col in df.columns if not col.endswith('_return')]
    
    # Calculer la volatilité glissante pour chaque ticker
    volatility_data = {}
    
    for ticker in volume_cols:
        if ticker in df.columns:
            # Calculer les rendements si pas déjà fait
            returns = df[ticker].pct_change().fillna(0)
            # Volatilité = écart-type glissant des rendements
            vol = returns.rolling(window=window, min_periods=1).std()
            volatility_data[f'{ticker}_volatility'] = vol
    
    # Créer DataFrame de volatilité
    volatility_df = pd.DataFrame(volatility_data, index=df.index)
    
    # Combiner avec les données existantes
    result = pd.concat([df, volatility_df], axis=1)
    
    return result

def get_ticker_data(df, ticker, data_type='volume'):
    """
    Extrait les données d'un ticker spécifique.
    
    Parameters:
    df: DataFrame principal
    ticker: nom du ticker (ex: '^DJI')
    data_type: 'volume', 'return', ou 'volatility'
    
    Returns:
    Series avec les données demandées
    """
    if data_type == 'volume':
        col_name = ticker
    elif data_type == 'return':
        col_name = f'{ticker}_return'
    elif data_type == 'volatility':
        col_name = f'{ticker}_volatility'
    else:
        raise ValueError("data_type doit être 'volume', 'return', ou 'volatility'")
    
    if col_name in df.columns:
        return df[col_name].dropna()
    else:
        print(f"Colonne {col_name} non trouvée. Colonnes disponibles: {df.columns.tolist()}")
        return pd.Series(dtype=float)

def get_available_tickers(df):
    """
    Retourne la liste des tickers disponibles (colonnes sans suffixe).
    """
    return [col for col in df.columns if not col.endswith(('_return', '_volatility'))]
