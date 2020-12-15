#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os # module permettant de communiquer avec le système d'exploitation sous-jacent.

chemin_actuel = os.path.dirname(os.path.abspath(__file__)) # stockage du chemin du fichier courant
templates = os.path.join(chemin_actuel, "templates") # stockage du chemin vers les templates
statics = os.path.join(chemin_actuel, "static") # stockage du chemin vers les statics

app = Flask(
    "Application",
    template_folder=templates,
    static_folder=statics,
) # instantiation de l'application dans la variable app et définition des dossiers templates et
  # statics en fonction des chemins os définis au-dessus.

# Import de la route principale depuis le fichier routes.py
from .routes import home