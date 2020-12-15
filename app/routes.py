#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
"""


# import des librairie
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from lxml import etree
import re


# import de l'application (app) depuis le fichier app.py
from .app import app


@app.route("/")
def home():
	return render_template("home.html")

@app.route("/monographie")
def monographie():
	return render_template("mono.html")