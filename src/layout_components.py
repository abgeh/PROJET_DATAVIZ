from dash import html, dcc

def create_header():
    """Crée l'en-tête principal de l'application avec titre et statistiques."""
    return html.Div([
        html.H1(
            "Impact des événements socio-politiques (2008–2023)",
            style={'textAlign':'center','marginBottom':'40px'}
        ),
        
        html.Div(className='intro-section', style={
            'textAlign':'center',
            'marginBottom':'40px'
        }, children=[
            html.P([
                "Explorez l'impact des événements géopolitiques majeurs sur les marchés financiers de ",
                html.Strong("2008 à 2023"), ". Découvrez comment les crises, élections et catastrophes naturelles ",
                "ont influencé les volumes d'échange des principaux indices mondiaux."
            ], style={'fontSize':'18px','lineHeight':'1.6','color':'#636e72'}),
            
            html.Div(className='stats-row', style={
                'display':'flex',
                'justifyContent':'space-around',
                'marginTop':'30px'
            }, children=[
                html.Div([
                    html.H3("10", style={'color':'var(--color-highlight)','margin':'0'}), 
                    html.P("Événements majeurs")
                ], className='stat-card'),
                html.Div([
                    html.H3("12", style={'color':'var(--color-highlight)','margin':'0'}), 
                    html.P("Indices analysés")
                ], className='stat-card'),
                html.Div([
                    html.H3("16", style={'color':'var(--color-highlight)','margin':'0'}), 
                    html.P("Années de données")
                ], className='stat-card'),
            ])
        ])
    ])

def create_volume_section(tickers_list):
    """Crée la section complète de visualisation du volume polaire."""
    return html.Div(className='viz-section', children=[
        html.H2("Volume d'échange journalier"),
        
        # Description explicative
        html.Div(className='section-intro', style={
            'backgroundColor': '#f8f9fa',
            'padding': '20px',
            'borderRadius': '8px',
            'marginBottom': '25px',
            'borderLeft': '4px solid var(--color-highlight)'
        }, children=[
            html.P([
                "Le ", html.Strong("volume d'échange"), " représente le nombre total d'actions ou de contrats échangés ",
                "sur une période donnée. Il constitue un indicateur clé de l'", html.Em("activité du marché"), " et de la ",
                html.Strong("réaction des investisseurs"), " face aux événements économiques et géopolitiques."
            ], style={'marginBottom': '12px', 'lineHeight': '1.5'}),
            
            html.P([
                "Cette visualisation polaire vous permet d'observer comment les volumes fluctuent au fil des mois ",
                "et d'identifier les périodes d'intense activité liées aux crises financières, élections, ",
                "ou autres événements marquants de 2008 à 2023."
            ], style={'marginBottom': '0', 'fontSize': '14px', 'color': '#6c757d', 'lineHeight': '1.4'})
        ]),

        # Contrôles interactifs
        _create_volume_controls(tickers_list),

        # Graphique principal
        dcc.Graph(id='volume-chart')
    ])

def _create_volume_controls(tickers_list):
    """Contrôles pour la visualisation volume : dropdown + slider."""
    return html.Div(className='control-group', style={'marginBottom': '30px'}, children=[
        
        # Sélection d'indice
        html.Div(style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'gap': '15px',
            'marginBottom': '25px',
            'padding': '15px',
            'backgroundColor': 'white',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'
        }, children=[
            html.Label("Sélectionnez un indice :", style={
                'fontWeight': '500',
                'color': '#495057',
                'fontSize': '15px'
            }),
            dcc.Dropdown(
                id='ticker-dropdown',
                options=[{'label': t, 'value': t} for t in tickers_list],
                value=tickers_list[0],
                clearable=False,
                style={'width': '200px', 'fontSize': '14px'}
            ),
        ]),

        # Slider de lissage avec description
        html.Div(style={
            'backgroundColor': 'white',
            'padding': '20px',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'
        }, children=[
            html.Div(style={'marginBottom': '15px'}, children=[
                html.Label("Lissage des données :", style={
                    'fontWeight': '500',
                    'color': '#495057',
                    'fontSize': '15px',
                    'marginRight': '10px'
                }),
                html.Span("Ajustez la fenêtre de lissage pour réduire les fluctuations quotidiennes", style={
                    'fontSize': '13px',
                    'color': '#6c757d',
                    'fontStyle': 'italic'
                })
            ]),
            
            html.Div(style={
                'display': 'flex',
                'alignItems': 'center',
                'gap': '20px',
                'marginTop': '10px'
            }, children=[
                html.Div(style={'flex': '1'}, children=[
                    dcc.Slider(
                        id='window-slider',
                        min=1, max=30, step=1, value=7,
                        marks={i: str(i) for i in [1, 7, 14, 30]},
                        tooltip={'placement': 'bottom', 'always_visible': False},
                        updatemode='drag'
                    )
                ]),
                html.Div(style={
                    'minWidth': '80px',
                    'textAlign': 'center',
                    'backgroundColor': '#e9ecef',
                    'padding': '8px 16px',
                    'borderRadius': '20px',
                    'fontSize': '14px',
                    'fontWeight': '600',
                    'color': '#495057'
                }, children=[
                    html.Span(id='window-value')
                ])
            ])
        ])
    ])

def create_choropleth_section(events_list):
    """Crée la section complète de visualisation choroplèthe."""
    return html.Div(className='viz-section', children=[
        html.H2("Impact géopolitique mondial"),

        # Description de la carte
        html.Div(className='section-intro', style={
            'backgroundColor': '#f8f9fa',
            'padding': '20px',
            'borderRadius': '8px',
            'marginBottom': '25px',
            'borderLeft': '4px solid var(--color-highlight)'
        }, children=[
            html.P([
                "Cette ", html.Strong("carte choroplèthe mondiale"), " révèle l'impact immédiat des événements géopolitiques ",
                "majeurs sur les ", html.Em("rendements boursiers régionaux"), ". En analysant les performances moyennes ",
                "des principaux indices de chaque continent (Amériques, Europe, Asie), elle met en lumière comment ",
                "les chocs géopolitiques se propagent différemment selon les zones économiques."
            ], style={'marginBottom': '12px', 'lineHeight': '1.5'}),
            
            html.P([
                "Les ", html.Strong("couleurs"), " reflètent l'intensité de l'impact : du ", 
                html.Strong("rouge foncé", style={'color': '#d63031'}), " (fortes pertes) au ", 
                html.Strong("vert foncé", style={'color': '#00b894'}), " (gains), en passant par le ",
                html.Strong("jaune", style={'color': '#fdcb6e'}), " (équilibre). L'échelle s'adapte automatiquement ",
                "à l'ampleur de chaque événement, révélant des impacts allant de quelques pour cent à des chutes dramatiques de 10% ou plus."
            ], style={'marginBottom': '12px', 'lineHeight': '1.5'}),
            
            html.P([
                "Survolez une région pour découvrir les indices analysés et leur performance précise. ",
                "Modifiez l'événement et la fenêtre d'analyse pour explorer comment différentes crises ",
                "affectent les marchés mondiaux avec des intensités et des délais variables."
            ], style={'marginBottom': '0', 'fontSize': '14px', 'color': '#6c757d', 'lineHeight': '1.4'})
        ]),
        
        # Contrôles interactifs
        _create_choropleth_controls(events_list),

        # Graphique principal
        dcc.Graph(id='choropleth-chart')
    ])
def _create_choropleth_controls(events_list):
    """Contrôles pour la carte choroplèthe : dropdown événements + slider fenêtre."""
    return html.Div(className='control-group', style={'marginBottom': '30px'}, children=[
        html.Div(style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'gap': '20px',
            'padding': '15px',
            'backgroundColor': 'white',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'
        }, children=[
            
            # Sélection d'événement
            html.Div(style={'flex': '1'}, children=[
                html.Label("Événement géopolitique :", style={
                    'fontWeight': '500',
                    'color': '#495057',
                    'fontSize': '15px',
                    'display': 'block',
                    'marginBottom': '5px'
                }),
                dcc.Dropdown(
                    id='choro-event-dropdown',
                    options=[{'label': n, 'value': n} for n in events_list],
                    value=events_list[-1],  # Dernier événement par défaut
                    clearable=False,
                    style={'fontSize': '14px'}
                ),
            ]),
            
            # Slider de fenêtre d'analyse
            html.Div(style={'flex': '0 0 250px'}, children=[
                html.Label("Fenêtre d'analyse :", style={
                    'fontWeight': '500',
                    'color': '#495057',
                    'fontSize': '15px',
                    'display': 'block',
                    'marginBottom': '5px'
                }),
                dcc.Slider(
                    id='choro-window-slider',
                    min=1, max=10, step=1, value=5,
                    marks={i: f"{i}j" for i in [1, 3, 5, 7, 10]},
                    tooltip={'placement': 'bottom', 'always_visible': True},
                    updatemode='drag'
                )
            ])
        ])
    ])

#visu2
def create_heatmap_section(events_list):
    """Crée la section complète de visualisation heatmap."""
    return html.Div(className='viz-section', children=[
        html.H2("Analyse temporelle des rendements"),

        # Description de la heatmap
        html.Div(className='section-intro', style={
            'backgroundColor': '#f8f9fa',
            'padding': '20px',
            'borderRadius': '8px',
            'marginBottom': '25px',
            'borderLeft': '4px solid var(--color-highlight)'
        }, children=[
            html.P([
                "Cette ", html.Strong("heatmap temporelle"), " examine l'évolution des rendements journaliers ",
                "des principaux indices boursiers ", html.Em("avant, pendant et après"), " un événement géopolitique. ",
                "Chaque ligne représente un indice, chaque colonne un jour relatif à l'événement ",
                "(jour 0 = date de l'événement)."
            ], style={'marginBottom': '12px', 'lineHeight': '1.5'}),
            
            html.P([
                "Les ", html.Strong("couleurs"), " révèlent l'intensité des réactions : ",
                html.Strong("rouge", style={'color': '#d63031'}), " pour les pertes, ",
                html.Strong("vert", style={'color': '#00b894'}), " pour les gains, et ",
                html.Strong("jaune", style={'color': '#fdcb6e'}), " pour la neutralité. ",
                "Cette visualisation permet d'identifier les patterns de réaction et de récupération des marchés."
            ], style={'marginBottom': '12px', 'lineHeight': '1.5'}),
            
            html.P([
                "Survolez une cellule pour voir les détails précis. La ligne verticale noire marque ",
                "le jour exact de l'événement, permettant d'observer l'impact immédiat et la propagation temporelle."
            ], style={'marginBottom': '0', 'fontSize': '14px', 'color': '#6c757d', 'lineHeight': '1.4'})
        ]),
        
        # Contrôles
        _create_heatmap_controls(events_list),

        # Graphique
        dcc.Graph(id='heatmap-chart')
    ])

def _create_heatmap_controls(events_list): 
    """Contrôles pour la heatmap : dropdown événements + slider fenêtre.""" 
    return html.Div(className='control-group', style={'marginBottom': '30px'}, 
                    children=[ html.Div(style={ 'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 
                                               'gap': '20px', 'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.05)' }, 
                                               children=[
                        # Sélection d'événement
                        html.Div(style={'flex': '1'}, children=[
                            html.Label("Événement à analyser :", style={
                                'fontWeight': '500',
                                'color': '#495057',
                                'fontSize': '15px',
                                'display': 'block',
                                'marginBottom': '5px'
                            }),
                            dcc.Dropdown(
                                id='heatmap-event-dropdown',
                                options=[{'label': n, 'value': n} for n in events_list],
                                value=events_list[0] if events_list else None,
                                clearable=False,
                                style={'fontSize': '14px'}
                            ),
                        ]),
                        
                        # Slider de fenêtre temporelle
                        html.Div(style={'flex': '0 0 280px'}, children=[
                            html.Label("Fenêtre temporelle (±jours) :", style={
                                'fontWeight': '500',
                                'color': '#495057',
                                'fontSize': '15px',
                                'display': 'block',
                                'marginBottom': '5px'
                            }),
                            dcc.Slider(
                                id='heatmap-window-slider',
                                min=3, max=14, step=1, value=7,
                                marks={i: f"±{i}" for i in [3, 5, 7, 10, 14]},
                                tooltip={'placement': 'bottom', 'always_visible': True},
                                updatemode='drag'
                            )
                        ])
                    ])
                ])

#visu 3
def create_volatility_section(events_list):
    """Crée la section complète de visualisation de volatilité."""
    return html.Div(className='viz-section', children=[
        html.H2("Évolution de la volatilité"),

        # Description de la volatilité
        html.Div(className='section-intro', style={
            'backgroundColor': '#f8f9fa',
            'padding': '20px',
            'borderRadius': '8px',
            'marginBottom': '25px',
            'borderLeft': '4px solid var(--color-highlight)'
        }, children=[
            html.P([
                "La ", html.Strong("volatilité"), " mesure l'instabilité des rendements d'un indice boursier. ",
                "Cette visualisation présente l'", html.Em("écart-type mobile"), " des rendements journaliers ",
                "calculé sur une fenêtre glissante, révélant comment l'incertitude des marchés évolue ",
                html.Strong("avant, pendant et après"), " un événement géopolitique."
            ], style={'marginBottom': '12px', 'lineHeight': '1.5'}),
            
            html.P([
                "Chaque ", html.Strong("courbe"), " trace l'évolution temporelle de la volatilité pour un indice ou un groupe d'indices. ",
                "Les ", html.Em("pics de volatilité"), " indiquent des périodes d'incertitude accrue, souvent liées aux réactions ",
                "immédiates des investisseurs face aux chocs externes. La ligne rouge marque le jour exact de l'événement."
            ], style={'marginBottom': '12px', 'lineHeight': '1.5'}),
            
            html.P([
                "Explorez différents groupements (indices individuels, régions, types d'actifs) et ajustez ",
                "la fenêtre d'analyse pour observer les patterns de volatilité caractéristiques de chaque type de crise."
            ], style={'marginBottom': '0', 'fontSize': '14px', 'color': '#6c757d', 'lineHeight': '1.4'})
        ]),
        
        # Contrôles
        _create_volatility_controls(events_list),

        # Graphique
        dcc.Graph(id='volatility-chart')
    ])

def _create_volatility_controls(events_list): 
    """Contrôles pour la volatilité : dropdown + slider unique + groupement."""
    return html.Div(className='control-group', style={'marginBottom': '30px'}, children=[
        
        # Une seule ligne avec tous les contrôles
        html.Div(style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'gap': '20px',
            'padding': '15px',
            'backgroundColor': 'white',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'
        }, children=[
            
            # Sélection d'événement
            html.Div(style={'flex': '1'}, children=[
                html.Label("Événement à analyser :", style={
                    'fontWeight': '500',
                    'color': '#495057',
                    'fontSize': '15px',
                    'display': 'block',
                    'marginBottom': '5px'
                }),
                dcc.Dropdown(
                    id='volatility-event-dropdown',
                    options=[{'label': n, 'value': n} for n in events_list],
                    value=events_list[0] if events_list else None,
                    clearable=False,
                    style={'fontSize': '14px'}
                ),
            ]),
            
            # Type de groupement
            html.Div(style={'flex': '1'}, children=[
                html.Label("Groupement des données :", style={
                    'fontWeight': '500',
                    'color': '#495057',
                    'fontSize': '15px',
                    'display': 'block',
                    'marginBottom': '5px'
                }),
                dcc.Dropdown(
                    id='volatility-grouping-dropdown',
                    options=[
                        {'label': 'Par région géographique', 'value': 'region'},
                        {'label': 'Indices individuels', 'value': 'individual'},
                        {'label': 'Actions vs Matières premières', 'value': 'type'}
                    ],
                    value='region',  # CHANGÉ: Par défaut région pour plus de variété
                    clearable=False,
                    style={'fontSize': '14px'}
                ),
            ]),
            
            # UNE SEULE fenêtre temporelle
            html.Div(style={'flex': '0 0 280px'}, children=[
                html.Label("Fenêtre d'analyse (±jours) :", style={
                    'fontWeight': '500',
                    'color': '#495057',
                    'fontSize': '15px',
                    'display': 'block',
                    'marginBottom': '5px'
                }),
                dcc.Slider(
                    id='volatility-window-slider',
                    min=3, max=14, step=1, value=7,
                    marks={i: f"±{i}" for i in [3, 5, 7, 10, 14]},
                    tooltip={'placement': 'bottom', 'always_visible': True},
                    updatemode='drag'
                )
            ])
        ])
    ])



def create_compare_section(categories):
    return html.Div([
        html.H3("Visualisation 5 : Rendements moyens ou volatilité par type d’actif"),
        dcc.Dropdown(
            id="compare-category-dropdown",
            options=[{"label": cat, "value": cat} for cat in categories],
            value=categories[0]
        ),
        dcc.RadioItems(
            id="compare-mode-radio",
            options=[
                {"label": "Rendement", "value": "return"},
                {"label": "Volatilité", "value": "volatility"}
            ],
            value="return",
            labelStyle={"display": "inline-block", "margin-right": "15px"}
        ),
        dcc.Graph(id="compare-graph")
    ], style={"marginBottom": "50px"})


