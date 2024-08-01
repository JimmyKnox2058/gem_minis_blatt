# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 14:54:25 2024

@author: Thomas
"""

import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H2('Das Projekt ist ein Lernprojekt, dessen Inhalt die Wortanalyse von ca. 2700 Ausgaben des gemeinsamen Ministerialblattes ist. Die gemeinsamen Ministerialblätter sind die seit 1950 von der Bundesregierung Deutschlands herausgegebenen Verwaltungsanweisungen - diese wurden auf der Website fragdenstaat.de als .pdf veröffentlicht.'),
    html.Div(['Teilaspekte, mit denen wir uns auseinandergesetzt haben, sind:', html.Br(), 
            html.Li("Beschaffung, Bereinigung und Verarbeitung der Textdaten"),  
            html.Li("Natural Language Processing"), 
            html.Li("statistische Methoden und Topic Modelling"), 
            html.Li("Darstellung der Ergebnisse mit Word Clouds, Graphen und Tabellen in einem Dashboard")
             ]),
])