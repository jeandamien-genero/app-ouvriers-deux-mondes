#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
author = Jean-Damien Généro
date = 2020-12-15
"""

import os
from flask import Flask


from .routes import home


chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")

app = Flask(
    "Application",
    template_folder=templates,
    static_folder=statics,
)
