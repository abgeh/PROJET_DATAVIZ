from dash import html, dcc

# ============================================================================== FONCTIONS PRINCIPALES  ======================================================================================

# =====EN-TËTE PRINCIPALE=====
def create_header():
    """Crée l'en-tête principal avec une introduction narrative captivante."""
    return html.Div([
        html.H1(
            "L'Impact des Événements Socio-Politiques sur les Marchés Financiers",
            style={'textAlign':'center','marginBottom':'30px', 'color': '#2c3e50'}
        ),
        
        html.Div(className='intro-section', style={
            'textAlign':'center',
            'marginBottom':'50px'
        }, children=[
            html.P([
                "De 2008 à 2023, notre monde a été secoué par des événements majeurs : ",
                "crises financières, pandémies, guerres, bouleversements politiques. Mais ",
                html.Em("comment ces chocs ont-ils réellement impacté"), " les marchés financiers mondiaux ?"
            ], style={'fontSize':'20px','lineHeight':'1.7','color':'#2c3e50', 'marginBottom': '20px'}),
            
            html.P([
                "Embarquez dans une exploration interactive qui révèle les réactions ",
                "surprenantes des investisseurs face à l'incertitude. Des volumes d'échange aux rendements, ",
                "de la volatilité aux différences régionales, découvrez ", html.Em("l'anatomie des chocs financiers"), "."
            ], style={'fontSize':'16px','lineHeight':'1.6','color':'#636e72', 'marginBottom': '30px'}),
            
            # Section statistiques détaillées
            html.Div(className='stats-detailed', style={
                'marginTop':'40px',
                'padding': '30px',
                'backgroundColor': '#f8f9fa',
                'borderRadius': '15px',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.05)'
            }, children=[
                
                # Titre de la section
                html.H3("📊 Panorama de notre exploration", style={
                    'textAlign': 'center',
                    'marginBottom': '30px',
                    'color': '#2c3e50',
                    'fontSize': '24px'
                }),
                
                # Grille des détails
                html.Div(style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(auto-fit, minmax(300px, 1fr))',
                    'gap': '25px',
                    'marginBottom': '20px'
                }, children=[
                    
                    # Événements détaillés avec tooltips
                    html.Div(style={
                        'backgroundColor': 'white',
                        'padding': '25px',
                        'borderRadius': '12px',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.08)',
                        'borderLeft': '4px solid #e74c3c'
                    }, children=[
                        html.H4("🌍 Événements analysés", style={
                            'color': '#e74c3c',
                            'marginBottom': '15px',
                            'fontSize': '18px'
                        }),
                        html.P("10 chocs majeurs qui ont marqué l'histoire :", style={
                            'fontSize': '14px',
                            'marginBottom': '12px',
                            'color': '#7f8c8d'
                        }),
                        html.Ul([
                            _create_event_item("Crise Lehman Brothers (2008)", "Faillite de la 4ème banque d'investissement américaine, déclenchant la crise financière mondiale"),
                            _create_event_item("Crise dette zone euro (2010)", "Crise de la dette souveraine en Europe, menaçant la stabilité de l'euro et de l'Union européenne"),
                            _create_event_item("Printemps arabe (2010)", "Vague de révolutions démocratiques au Moyen-Orient à l'origine d'une instabilité géopolitique majeure"),
                            _create_event_item("Fukushima (2011)", "Catastrophe nucléaire au Japon suite au tsunami qui a remit en question l'énergie nucléaire mondiale"),
                            _create_event_item("Brexit (2016)", "Référendum britannique pour quitter l'UE, laissant derrière lui une incertitude économique et politique durable"),
                            _create_event_item("Élection Trump (2016)", "Victoire surprise créant des incertitudes sur les politiques commerciales et géopolitiques américaines"),
                            _create_event_item("Guerre commerciale US-CN (2018)", "Escalade des tarifs douaniers entre les deux premières économies mondiales"),
                            _create_event_item("Assassinat Soleimani (2020)", "Élimination du général iranien et risque d'un conflit militaire au Moyen-Orient"),
                            _create_event_item("COVID-19 (2020)", "Pandémie mondiale provoquant des confinements et la plus grave récession depuis 1929"),
                            _create_event_item("Invasion Ukraine (2022)", "Guerre en Europe qui a relancé les tensions géopolitiques et créé une crise énergétique")
                        ], style={
                            'fontSize': '13px',
                            'lineHeight': '1.4',
                            'paddingLeft': '18px',
                            'color': '#2c3e50',
                            'listStyle': 'none'
                        })
                    ]),
                    
                    # Indices détaillés avec tooltips
                    html.Div(style={
                        'backgroundColor': 'white',
                        'padding': '25px',
                        'borderRadius': '12px',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.08)',
                        'borderLeft': '4px solid #3498db'
                    }, children=[
                        html.H4("📈 Indices surveillés", style={
                            'color': '#3498db',
                            'marginBottom': '15px',
                            'fontSize': '18px'
                        }),
                        html.P("12 baromètres des marchés mondiaux :", style={
                            'fontSize': '14px',
                            'marginBottom': '12px',
                            'color': '#7f8c8d'
                        }),
                        html.Ul([
                            _create_index_item("Shanghai Composite (000001.SS)", "Indice composite de Shanghai, reflet du marché chinois"),
                            _create_index_item("BSE Sensex (^BSESN)", "Plus ancien indice indien, baromètre historique de la Bourse de Bombay"),
                            _create_index_item("Nifty 50 (^NSEI)", "Indice principal de la Bourse nationale indienne, 50 plus grandes capitalisations"),
                            _create_index_item("Nikkei 225 (^N225)", "Principal indice japonais, indicateur de la 3ème économie mondiale"),
                            _create_index_item("Dow Jones (^DJI)", "Plus ancien indice américain, suit 30 entreprises industrielles emblématiques"),
                            _create_index_item("S&P 500 (^GSPC)", "Indice des 500 plus grandes entreprises américaines, référence mondiale"),
                            _create_index_item("NASDAQ Composite (^IXIC)", "Indice technologique américain regroupant toutes les entreprises du NASDAQ"),
                            _create_index_item("NYSE Composite (^NYA)", "Indice composite de la Bourse de New York, reflétant l'ensemble du marché américain"),     
                            _create_index_item("FTSE 100 (^FTSE)", "Indice des 100 plus grandes entreprises britanniques cotées à Londres"),                     
                            _create_index_item("Euronext 100 (^N100)", "Indice paneuropéen des 100 plus grandes entreprises d'Europe"),                          
                            _create_index_item("Or Futures (GC=F)", "Contrats à terme sur l'or, valeur refuge traditionnelle contre l'inflation"),
                            _create_index_item("Pétrole Futures (CL=F)", "Contrats à terme sur le pétrole brut, indicateur géopolitique crucial")
                        ], style={
                            'fontSize': '13px',
                            'lineHeight': '1.4',
                            'paddingLeft': '18px',
                            'color': '#2c3e50',
                            'listStyle': 'none'
                        })
                    ]),
                                          
                ])
            ])

        ])
    ])

# =====VIS 1) VOLUME=====
def create_volume_section(tickers_list):
    """Première étape du storytelling : vue d'ensemble par le volume."""
    return html.Div(className='viz-section', children=[
        html.H2("Commençons par le commencement : L'activité des marchés"),
        
        html.Div(className='section-intro', style={
            'backgroundColor': '#f8f9fa',
            'padding': '25px',
            'borderRadius': '10px',
            'marginBottom': '30px',
            'borderLeft': '5px solid #0984e3'
        }, children=[
            html.P([
                "Notre voyage débute par une découverte intéressante : contrairement aux idées reçues, ",
                "les ", html.Em("crises ne paralysent pas"), " les marchés. Au contraire ! Elles les électrisent."
            ], style={'marginBottom': '15px', 'lineHeight': '1.6', 'fontSize': '16px'}),
            
            html.P([
                "Le volume d'échange - ce nombre d'actions qui changent de mains chaque jour - ",
                "devient notre première boussole. Quand l'incertitude frappe, les investisseurs ne fuient pas : ",
                "ils ", html.Em("réagissent massivement"), ". Ventes de panique et achats stratégiques s'entremêlent."
            ], style={'marginBottom': '15px', 'lineHeight': '1.6'}),
            
            html.P([
                "📊 Cette visualisation polaire condense 15 années d'histoire financière ",
                " en un cercle hypnotique. Chaque pic révèle un moment où le monde a retenu son souffle..."
            ], style={'marginBottom': '0', 'fontSize': '15px', 'color': '#636e72', 'fontStyle': 'italic'})
        ]),

        _create_volume_controls(tickers_list),
        dcc.Graph(id='volume-chart')
    ])

# =====VIS 2) HEATMAP DES RENDEMENTS=====
def create_heatmap_section(events_list):
    """Deuxième étape : plongée dans le détail des rendements."""
    return html.Div(className='viz-section', children=[
        html.H2("Maintenant, plongeons dans l'intimité des marchés"),

        html.Div(className='section-intro', style={
            'backgroundColor': '#f8f9fa',
            'padding': '25px',
            'borderRadius': '10px',
            'marginBottom': '30px',
            'borderLeft': '5px solid #e17055'
        }, children=[
            html.P([
                "Le volume nous a montré ", html.Em("quand"), " les marchés s'agitent. Mais que se passe-t-il ",
                "concrètement ? Cette heatmap révèle l'anatomie précise des chocs financiers."
            ], style={'marginBottom': '15px', 'lineHeight': '1.6', 'fontSize': '16px'}),
            
            html.P([
                "Imaginez pouvoir remonter le temps et observer, jour par jour, comment chaque ",
                "indice mondial a réagi. Du rouge sang des pertes catastrophiques au ",
                "vert espoir des rebonds spectaculaires, chaque cellule raconte une histoire."
            ], style={'marginBottom': '15px', 'lineHeight': '1.6'}),
            
            html.P([
                "🎯 La ligne verticale marque le ", html.Em("jour J"), " - l'instant où tout bascule. ",
                "Observez comment l'onde de choc se propage, et les patterns cachés ",
                " des réactions en chaîne."
            ], style={'marginBottom': '0', 'fontSize': '15px', 'color': '#636e72', 'fontStyle': 'italic'})
        ]),
        
        _create_heatmap_controls(events_list),
        dcc.Graph(id='heatmap-chart')
    ])

# =====VIS 3) VOLATILITE=====
def create_volatility_section(events_list):
    """Troisième étape : exploration de l'incertitude."""
    return html.Div(className='viz-section', children=[
        html.H2("Allons plus loin : Mesurer la peur des investisseurs"),

        html.Div(className='section-intro', style={
            'backgroundColor': '#f8f9fa',
            'padding': '25px',
            'borderRadius': '10px',
            'marginBottom': '30px',
            'borderLeft': '5px solid #a29bfe'
        }, children=[
            html.P([
                "Les rendements nous ont révélé les ", html.Em("gains et pertes"), ". Mais comment mesurer ",
                "l'angoisse des marchés ? Bienvenue dans l'univers de la volatilité !"
            ], style={'marginBottom': '15px', 'lineHeight': '1.6', 'fontSize': '16px'}),
            
            html.P([
                "La volatilité capture quelque chose d'invisible mais crucial : le ",
                html.Em("niveau de stress"), " des investisseurs. Plus les cours zigzaguent violemment, ",
                "plus l'incertitude règne. C'est le pouls des marchés financiers."
            ], style={'marginBottom': '15px', 'lineHeight': '1.6'}),
            
            html.P([
                "🌊 Chaque courbe trace l'évolution de cette nervosité. Observez les pics d'anxiété ",
                " qui précèdent ou suivent les événements, révélant que parfois, ",
                html.Em("l'anticipation fait plus mal que la réalité"), "..."
            ], style={'marginBottom': '0', 'fontSize': '15px', 'color': '#636e72', 'fontStyle': 'italic'})
        ]),
        
        _create_volatility_controls(events_list),
        dcc.Graph(id='volatility-chart')
    ])

# ====== VIS 4) CHOROPLETH ===
def create_choropleth_section(events_list):
    """Dernière étape : vision géographique finale."""
    return html.Div(className='viz-section', children=[
        html.H2(" Prenons maintenant de la hauteur : Le monde face à la crise"),

        html.Div(className='section-intro', style={
            'backgroundColor': '#f8f9fa',
            'padding': '25px',
            'borderRadius': '10px',
            'marginBottom': '30px',
            'borderLeft': '5px solid #00b894'
        }, children=[
            html.P([
                "🌍 prenons de la hauteur ! Cette carte mondiale ",
                "révèle une leçon fondamentale de l'économie globalisée : ", 
                html.Em("la géographie compte encore"), "."
            ], style={'marginBottom': '15px', 'lineHeight': '1.6', 'fontSize': '16px'}),
            
            html.P([
                "Quand l'Ukraine est envahie, l'Europe souffre mais l'Amérique résiste. ",
                "Quand Wall Street s'effondre, le monde entier tremble. Cette carte raconte l'histoire des ",
                html.Em("interconnexions"), " et des vulnérabilités régionales."
            ], style={'marginBottom': '15px', 'lineHeight': '1.6'}),
            
            
            html.P([
                "✨ ", html.Em("Votre exploration touche à sa fin"), ". Vous avez désormais les clés pour ",
                "comprendre comment les marchés financiers respirent au rythme du monde."
            ], style={'marginBottom': '0', 'fontSize': '15px', 'color': '#636e72', 'fontStyle': 'italic'})
        ]),
        
        _create_choropleth_controls(events_list),
        dcc.Graph(id='choropleth-chart')
        
    ])

# ====== VIS 5) COMPARE ===
def create_compare_section(categories_list):
    """Avant-dernière étape : synthèse comparative."""
    return html.Div(className='viz-section', children=[
        html.H2("⚖️ Pour conclure notre exploration : La grande comparaison"),

        html.Div(className='section-intro', style={
            'backgroundColor': '#f8f9fa',
            'padding': '25px',
            'borderRadius': '10px',
            'marginBottom': '30px',
            'borderLeft': '5px solid #fd79a8'
        }, children=[
            html.P([
                " Nous avons exploré le ", html.Em("quand"), ", le ", html.Em("comment"), " et le ", html.Em("combien"), 
                ". Mais voici la question ultime : tous les chocs se valent-ils ?"
            ], style={'marginBottom': '15px', 'lineHeight': '1.6', 'fontSize': '16px'}),
            
            html.P([
                "Cette visualisation révèle une vérité surprenante : crises sanitaires, ",
                "tensions géopolitiques, bouleversements politiques et ",
                "krachs financiers n'affectent pas les marchés de la même manière !"
            ], style={'marginBottom': '15px', 'lineHeight': '1.6'}),
            
            html.P([
                "🔍 Découvrez qui remporte la palme du ", html.Em("chaos maximal"), " et observez comment ",
                "les matières premières (or, pétrole) dansent différemment des ",
                "indices boursiers face à l'adversité."
            ], style={'marginBottom': '0', 'fontSize': '15px', 'color': '#636e72', 'fontStyle': 'italic'})
        ]),
        
        _create_compare_controls(categories_list),
        dcc.Graph(id='compare-chart'),

               # Conclusion finale
        html.Div(style={
            'backgroundColor': '#2c3e50',
            'color': 'white',
            'padding': '30px',
            'borderRadius': '10px',
            'marginTop': '40px',
            'textAlign': 'center'
        }, children=[
            html.H3("🚀 Votre voyage dans l'univers des marchés financiers s'achève ici", 
                   style={'marginBottom': '20px', 'color': '#74b9ff'}),
            html.P([
                "Vous avez découvert comment 10 événements majeurs ont façonné ",
                "16 années d'histoire financière. De la panique aux opportunités, ",
                "des volumes aux rendements, vous maîtrisez désormais ", 
                html.Em("l'art de lire les émotions des marchés"), "."
            ], style={'fontSize': '16px', 'lineHeight': '1.6', 'marginBottom': '20px'}),
            html.P([
                "💡 La prochaine fois qu'un événement mondial fera trembler les marchés, ",
                "vous saurez décrypter les signaux et comprendre que derrière chaque ",
                "courbe se cache une histoire humaine fascinante."
            ], style={'fontSize': '14px', 'lineHeight': '1.5', 'color': '#ddd'})
        ])
    ])


# ============================================================================== FONCTIONS DE CONTRÔLES  ======================================================================================

#===== CONTRÔLES POUR LA VISUALISATION DU VOLUME  =====
def _create_volume_controls(tickers_list):
    """Contrôles pour la visualisation volume : dropdown + slider."""
    return html.Div(className='control-group', style={'marginBottom': '30px'}, children=[
        
        # Selection d'indice
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
            html.Label("Indice exploré :", style={
                'fontWeight': '500',
                'color': '#495057',
                'fontSize': '15px'
            }),
            dcc.Dropdown(
                id='ticker-dropdown',
                options=_create_ordered_ticker_options(tickers_list),
                value=_get_first_available_ticker(tickers_list),
                clearable=False,
                style={'width': '350px', 'fontSize': '14px'}  # Plus large pour les noms complets
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
                html.Label("Fenêtre d'observation :", style={
                    'fontWeight': '500',
                    'color': '#495057',
                    'fontSize': '15px',
                    'marginRight': '10px'
                }),
                html.Span("Ajustez la fenêtre pour révéler les tendances cachées", style={
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
                        min=1, max=14, step=1, value=7,
                        marks={i: str(i) for i in [1, 7, 14]},
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

#===== CONTRÔLES POUR LA VISUALISATION DE LA HEATMAP DES RENDEMENTS  =====
def _create_heatmap_controls(events_list): 
    """Contrôles pour la heatmap : dropdown evenements + slider fenêtre.""" 
    return html.Div(className='control-group', style={'marginBottom': '30px'}, 
                    children=[ html.Div(style={ 'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 
                                               'gap': '20px', 'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.05)' }, 
                                               children=[
                        html.Div(style={'flex': '1'}, children=[
                            html.Label("Événement sélectionné:", style={
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
                        
                        html.Div(style={'flex': '0 0 280px'}, children=[
                            html.Label("Fenêtre d'observation:", style={
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

#===== CONTRÔLES POUR LA VISUALISATION DE LA VOLATILITÉ  =====
def _create_volatility_controls(events_list): 
    """Contrôles pour la volatilité : 3 éléments parfaitement alignés horizontalement."""
    return html.Div(className='control-group', style={'marginBottom': '30px'}, children=[
        
        # Une seule ligne avec alignement parfait des labels
        html.Div(style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'flex-start',  # IMPORTANT: Aligne le haut des conteneurs
            'gap': '20px',
            'padding': '15px',
            'backgroundColor': 'white',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'
        }, children=[
            
            # Événement à disséquer
            html.Div(style={'flex': '1', 'minWidth': '200px'}, children=[
                html.Label("Événement sélectionné :", style={
                    'fontWeight': '500',
                    'color': '#495057',
                    'fontSize': '15px',
                    'display': 'block',
                    'marginBottom': '5px',
                    'height': '20px',  # FIXÉ: Hauteur fixe pour alignement
                    'lineHeight': '20px'  # AJOUTÉ: Alignement vertical du texte
                }),
                dcc.Dropdown(
                    id='volatility-event-dropdown',
                    options=[{'label': n, 'value': n} for n in events_list],
                    value=events_list[0] if events_list else None,
                    clearable=False,
                    style={'fontSize': '14px'}
                ),
            ]),
            
            # Angle d'analyse
            html.Div(style={'flex': '0 0 180px'}, children=[
                html.Label("Angle d'analyse :", style={
                    'fontWeight': '500',
                    'color': '#495057',
                    'fontSize': '15px',
                    'display': 'block',
                    'marginBottom': '5px',
                    'height': '20px',  # FIXÉ: Même hauteur que les autres
                    'lineHeight': '20px'  # AJOUTÉ: Alignement vertical du texte
                }),
                dcc.Dropdown(
                    id='volatility-grouping-dropdown',
                    options=[
                        {'label': 'Par région', 'value': 'region'},
                        {'label': 'Individuels', 'value': 'individual'},
                        {'label': 'Actions vs Commodités', 'value': 'type'}
                    ],
                    value='region',
                    clearable=False,
                    style={'fontSize': '14px'}
                ),
            ]),
            
            # Période d'étude
            html.Div(style={'flex': '0 0 320px'}, children=[
                html.Label("Fenêtre d'observation :", style={
                    'fontWeight': '500',
                    'color': '#495057',
                    'fontSize': '15px',
                    'display': 'block',
                    'marginBottom': '5px',
                    'height': '20px',  # FIXÉ: Même hauteur que les autres
                    'lineHeight': '20px'  # AJOUTÉ: Alignement vertical du texte
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

#===== CONTRÔLES POUR LA CARTE CHOROPLÈTHE  =====def _create_choropleth_controls(events_list):
    """Contrôles pour la carte choroplèthe : 2 éléments parfaitement alignés horizontalement."""
    return html.Div(className='control-group', style={'marginBottom': '30px'}, children=[
        html.Div(style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'flex-start',  # IMPORTANT: Aligne le haut des conteneurs
            'gap': '20px',
            'padding': '15px',
            'backgroundColor': 'white',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'
        }, children=[
            
            # Événement mondial à explorer
            html.Div(style={'flex': '1', 'minWidth': '250px'}, children=[
                html.Label("Événement sélectionné :", style={
                    'fontWeight': '500',
                    'color': '#495057',
                    'fontSize': '15px',
                    'display': 'block',
                    'marginBottom': '5px',
                    'height': '20px',  # FIXÉ: Hauteur fixe pour alignement
                    'lineHeight': '20px'  # AJOUTÉ: Alignement vertical du texte
                }),
                dcc.Dropdown(
                    id='choro-event-dropdown',
                    options=[{'label': n, 'value': n} for n in events_list],
                    value=events_list[-1],
                    clearable=False,
                    style={'fontSize': '14px'}
                ),
            ]),
            
            # Durée d'observation
            html.Div(style={'flex': '0 0 300px'}, children=[
                html.Label("Fenêtre d'observation :", style={
                    'fontWeight': '500',
                    'color': '#495057',
                    'fontSize': '15px',
                    'display': 'block',
                    'marginBottom': '5px',
                    'height': '20px',  # FIXÉ: Même hauteur que l'autre
                    'lineHeight': '20px'  # AJOUTÉ: Alignement vertical du texte
                }),
                dcc.Slider(
                    id='choro-window-slider',
                    min=1, max=14, step=1, value=5,
                    marks={i: f"{i}j" for i in [1, 3, 5, 7, 10, 14]},
                    tooltip={'placement': 'bottom', 'always_visible': True},
                    updatemode='drag'
                )
            ])
        ])
    ])

#===== CONTRÔLES POUR LA CARTE CHOROPLÈTHE  =====
def _create_choropleth_controls(events_list):
    """Contrôles pour la carte choroplèthe : 2 éléments parfaitement alignés horizontalement."""
    return html.Div(className='control-group', style={'marginBottom': '30px'}, children=[
        html.Div(style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'flex-start',  # IMPORTANT: Aligne le haut des conteneurs
            'gap': '20px',
            'padding': '15px',
            'backgroundColor': 'white',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'
        }, children=[
            
            # Événement mondial à explorer
            html.Div(style={'flex': '1', 'minWidth': '250px'}, children=[
                html.Label("Événement mondial à explorer :", style={
                    'fontWeight': '500',
                    'color': '#495057',
                    'fontSize': '15px',
                    'display': 'block',
                    'marginBottom': '5px',
                    'height': '20px',  # FIXÉ: Hauteur fixe pour alignement
                    'lineHeight': '20px'  # AJOUTÉ: Alignement vertical du texte
                }),
                dcc.Dropdown(
                    id='choro-event-dropdown',
                    options=[{'label': n, 'value': n} for n in events_list],
                    value=events_list[-1],
                    clearable=False,
                    style={'fontSize': '14px'}
                ),
            ]),
            
            # Durée d'observation
            html.Div(style={'flex': '0 0 300px'}, children=[
                html.Label("Durée d'observation :", style={
                    'fontWeight': '500',
                    'color': '#495057',
                    'fontSize': '15px',
                    'display': 'block',
                    'marginBottom': '5px',
                    'height': '20px',  # FIXÉ: Même hauteur que l'autre
                    'lineHeight': '20px'  # AJOUTÉ: Alignement vertical du texte
                }),
                dcc.Slider(
                    id='choro-window-slider',
                    min=1, max=14, step=1, value=5,
                    marks={i: f"{i}j" for i in [1, 3, 5, 7, 10, 14]},
                    tooltip={'placement': 'bottom', 'always_visible': True},
                    updatemode='drag'
                )
            ])
        ])
    ])

#===== CONTRÔLES POUR LA COMPARAISON DES CRISES  =====
def _create_compare_controls(categories_list): 
    """Contrôles pour la comparaison : catégorie + métrique + fenêtre."""
    return html.Div(className='control-group', style={'marginBottom': '30px'}, 
                    children=[ html.Div(style={ 'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'gap': '20px', 'padding': '15px',
                                                'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.05)' }, 
                                                children=[
            html.Div(style={'flex': '1'}, children=[
                html.Label("Type de crise à analyser :", style={
                    'fontWeight': '500',
                    'color': '#495057',
                    'fontSize': '15px',
                    'display': 'block',
                    'marginBottom': '5px'
                }),
                dcc.Dropdown(
                    id='compare-category-dropdown',
                    options=[{'label': cat, 'value': cat} for cat in categories_list],
                    value=categories_list[0] if categories_list else None,
                    clearable=False,
                    style={'fontSize': '14px'}
                ),
            ]),
            
            html.Div(style={'flex': '1'}, children=[
                html.Label("Métrique d'analyse :", style={
                    'fontWeight': '500',
                    'color': '#495057',
                    'fontSize': '15px',
                    'display': 'block',
                    'marginBottom': '5px'
                }),
                dcc.RadioItems(
                    id='compare-mode-radio',
                    options=[
                        {'label': ' Performance (rendements)', 'value': 'return'},
                        {'label': ' Nervosité (volatilité)', 'value': 'volatility'}
                    ],
                    value='return',
                    style={'fontSize': '14px'},
                    labelStyle={'display': 'block', 'marginBottom': '5px'}
                )
            ]),
            
            html.Div(style={'flex': '0 0 280px'}, children=[
                html.Label("Fenêtre d'impact :", style={
                    'fontWeight': '500',
                    'color': '#495057',
                    'fontSize': '15px',
                    'display': 'block',
                    'marginBottom': '5px'
                }),
                dcc.Slider(
                    id='compare-window-slider',
                    min=0, max=14, step=1, value=0,
                    marks={
                        0: 'Jour J',
                        1: '±1j',
                        3: '±3j', 
                        5: '±5j',
                        7: '±7j',
                        10: '±10j',
                        14: '±14j'
                    },
                    tooltip={'placement': 'bottom', 'always_visible': True},
                    updatemode='drag'
                )
            ])
        ])
    ])



# =================================================================================== FONCTIONS ANNEXES  ========================================================================================

def _create_event_item(name, description):
    """Crée un élément de liste d'événement avec tooltip."""
    return html.Li([
        html.Span("• ", style={'marginRight': '8px', 'color': '#e74c3c'}),
        html.Span(name, style={'marginRight': '8px'}),
        html.Span("ℹ️", style={
            'fontSize': '12px',
            'cursor': 'pointer',
            'color': '#3498db',
            'position': 'relative'
        }, title=description)
    ], style={
        'marginBottom': '6px',
        'display': 'flex',
        'alignItems': 'center'
    })

def _create_index_item(name, description):
    """Crée un élément de liste d'indice avec tooltip."""
    return html.Li([
        html.Span("• ", style={'marginRight': '8px', 'color': '#3498db'}),
        html.Span(name, style={'marginRight': '8px'}),
        html.Span("ℹ️", style={
            'fontSize': '12px',
            'cursor': 'pointer',
            'color': '#e67e22',
            'position': 'relative'
        }, title=description)
    ], style={
        'marginBottom': '6px',
        'display': 'flex',
        'alignItems': 'center'
    })

def _create_ordered_ticker_options(tickers_list):
    """Crée les options du dropdown dans l'ordre exact de l'introduction."""
    
    # Ordre exact de l'introduction
    ordered_tickers = [
        ('000001.SS', 'Shanghai Composite (000001.SS)'),
        ('^BSESN', 'BSE Sensex (^BSESN)'),
        ('^NSEI', 'Nifty 50 (^NSEI)'),
        ('^N225', 'Nikkei 225 (^N225)'),
        ('^DJI', 'Dow Jones (^DJI)'),
        ('^GSPC', 'S&P 500 (^GSPC)'),
        ('^IXIC', 'NASDAQ Composite (^IXIC)'),
        ('^NYA', 'NYSE Composite (^NYA)'),
        ('^FTSE', 'FTSE 100 (^FTSE)'),
        ('^N100', 'Euronext 100 (^N100)'),
        ('GC=F', 'Or Futures (GC=F)'),
        ('CL=F', 'Pétrole Futures (CL=F)')
    ]
    
    # Créer les options seulement pour les tickers disponibles, dans l'ordre voulu
    options = []
    for ticker_code, display_name in ordered_tickers:
        if ticker_code in tickers_list:
            options.append({
                'label': display_name,
                'value': ticker_code
            })
    
    return options

def _get_first_available_ticker(tickers_list):
    """Retourne le premier ticker disponible selon l'ordre de l'introduction."""
    
    # Ordre de priorité (même que l'introduction)
    priority_order = [
        '000001.SS', '^BSESN', '^NSEI', '^N225', '^DJI', '^GSPC', 
        '^IXIC', '^NYA', '^FTSE', '^N100', 'GC=F', 'CL=F'
    ]
    
    # Retourner le premier ticker trouvé dans l'ordre de priorité
    for ticker in priority_order:
        if ticker in tickers_list:
            return ticker
    
    # Fallback au premier ticker disponible si aucun de l'ordre n'est trouvé
    return tickers_list[0] if tickers_list else None

