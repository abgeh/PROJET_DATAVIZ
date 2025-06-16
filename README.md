# Impact des Événements Socio-Politiques sur les Marchés Financiers

Une application interactive qui révèle comment les crises mondiales façonnent les marchés financiers à travers 5 visualisations immersives.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Dash](https://img.shields.io/badge/Dash-2.0+-green.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## À propos du projet

Cette application analyse l'impact de **10 événements géopolitiques majeurs** (2008-2023) sur **12 indices financiers mondiaux**. À travers un parcours narratif interactif, découvrez comment les crises financières, pandémies, guerres et bouleversements politiques influencent les marchés.

### Événements analysés
- **Crise Lehman Brothers** (2008) - Effondrement financier mondial
- **Crise dette zone euro** (2010) - Crise souveraine européenne
- **Printemps arabe** (2010) - Révolutions au Moyen-Orient  
- **Fukushima** (2011) - Catastrophe nucléaire
- **Brexit** (2016) - Sortie du Royaume-Uni de l'UE
- **Élection Trump** (2016) - Changement géopolitique US
- **Guerre commerciale US-Chine** (2018) - Tensions économiques
- **Assassinat Soleimani** (2020) - Escalade Iran-USA
- **COVID-19** (2020) - Pandémie mondiale
- **Invasion Ukraine** (2022) - Conflit européen

### Indices surveillés
- **Amériques** : S&P 500, Dow Jones, NASDAQ, NYSE Composite
- **Europe** : FTSE 100, Euronext 100
- **Asie** : Nikkei 225, Shanghai Composite, Nifty 50, BSE Sensex
- **Matières premières** : Or, Pétrole WTI


## Fonctionnalités principales

### 1. **Volume Polaire Interactif**
Visualisation chronologique des volumes d'échange sous forme de graphique polaire révélant les pics d'activité lors des crises.

### 2. **Heatmap des Rendements**
Carte thermique montrant l'impact jour par jour des événements sur tous les indices mondiaux.

### 3. **Analyse de Volatilité**
Évolution du stress des marchés avec groupements par région, type d'actif ou indices individuels.

### 4. **Carte Choroplèthe Mondiale**
Visualisation géographique des impacts régionaux révélant les vulnérabilités économiques.

### 5. **Comparaison des Crises**
Analyse comparative par catégorie d'événement (économique, géopolitique, sanitaire, politique).

## Installation

### Prérequis
- Python 3.8+
- pip ou conda

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/abgeh/PROJET_DATAVIZ.git
cd PROJET_DATAVIZ
```

2. **Créer un environnement virtuel (recommandé)**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Préparer les données**
- Placez vos fichiers CSV dans le dossier `data/`
- Format attendu : `*_Global_Markets_Data.csv`

5. **Lancer l'application**
```bash
python app.py
```
. **Accédez à l'interface**
- Ouvrez [http://localhost:8050](http://localhost:8050) dans votre navigateur.


## Structure du projet

```
marches-geopolitique/
├── app.py                              # Application principale Dash
├── data_loader.py                      # Chargement des données financières
├── data_processor.py                   # Calculs rendements/volatilité
├── layout_components.py                # Interface utilisateur
├── callbacks.py                        # Interactions utilisateur
├── viz_volume.py                       # Visualisation polaire volumes
├── viz_heatmap.py                      # Heatmap des rendements
├── viz_volatility.py                   # Graphiques de volatilité
├── viz_choropleth.py                   # Carte choroplèthe mondiale
├── viz_compare.py                      # Comparaisons par catégorie
├── config/
│   ├── events.json                     # Configuration des événements
│   └── tickers.json                    # Configuration des indices
├── data/                               # Données financières (CSV)
│   ├── 2008_Global_Markets_Data.csv    
│   └── 20[...]_Global_Markets_Data.csv    
│   └── 2023_Global_Markets_Data.csv    
├── requirements.txt                    # Dépendances Python
└── README.md                           # Documentation
```

## Utilisation

### Navigation interactive
1. **Commencez par la vue volume** pour comprendre l'activité globale
2. **Explorez la heatmap** pour voir les impacts détaillés  
3. **Analysez la volatilité** pour mesurer le stress des marchés
4. **Examinez la carte mondiale** pour les effets géographiques
5. **Comparez les crises** pour identifier les patterns

### Contrôles disponibles
- **Sélection d'événements** : Dropdown avec 10 crises majeures
- **Fenêtres temporelles** : ±1 à ±14 jours autour des événements
- **Groupements** : Par région, type d'actif, ou indices individuels
- **Métriques** : Rendements ou volatilité selon l'analyse souhaitée



## Auteurs

- **Ahmed Baba GAH EL HILAL** - *Développement* - 
- **Sofiane MOUALDI** - *Développement* - 
- **Evan BLANC** - *Développement* - 
- **Othmane LAKHDAR** - *Développement* - 
- **Ali MOUCHAHID** - *Développement* - 
- **Farid BABA** - *Développement* - 

## Remerciements

- **Plotly/Dash** pour le framework de visualisation
- **Pavan Narne sur Kaggle**  pour les données : https://www.kaggle.com/datasets/pavankrishnanarne/global-stock-market-2008-present?select=2023_Global_Markets_Data.csv



