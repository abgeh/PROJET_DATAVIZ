import glob
import pandas as pd

def load_market_data(data_dir="data", pattern="*_Global_Markets_Data.csv"):
    """
    Lit tous les CSV du dossier data_dir correspondant à pattern,
    parse les dates, et renvoie un DataFrame unifié.
    """
    files = glob.glob(f"{data_dir}/{pattern}")
    if not files:
        raise FileNotFoundError(f"Aucun CSV trouvé dans {data_dir} avec {pattern}")
    df = pd.concat((pd.read_csv(f, parse_dates=['Date']) for f in files),
                   ignore_index=True)
    # trier, dropna, typer col
    df = df.sort_values(['Ticker', 'Date'])
    df = df.dropna(subset=['Close','Volume'])
    return df
