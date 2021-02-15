#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
author = Jean-Damien Généro
date = 2020-12-15
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")


app = Flask(
    "Application",
    template_folder=templates,
    static_folder=statics,
)

# Configuration de la base de donnée
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./od2m_bdd.sqlite'
# stockage de la base dans l'objet db
db = SQLAlchemy(app)

from .routes import home
