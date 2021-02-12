#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
author = Jean-Damien Généro
date = 2020-12-15
"""

# libraries
import csv
import os
import re
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from lxml import etree

from .app import app
from .clear_xml import clear_file
from .database_init import get_filenames, tables_init
from .modeles.data import Type, Subtype



tables_init(get_filenames("./app/static/xml", ".xml"))


# routes
@app.route("/")
def home():
    """Route that loads the home page.
    """
    return render_template("home.html")

@app.route("/monographies")
def monographies():
    """Route that loads a page with the monographs list out of a CSV.
    Works with a dictionary where monographs' titles are keys and XML
    filenames are values.
    """
    with open("../app-ouvriers-deux-mondes/app/static/csv/id_monographies.csv") as csv_file:
        file = csv.reader(csv_file)
        dict_mono = {}
        for row in file:
            dict_mono[row[3]] = [row[0], row[2]]
        del dict_mono['Titres']
    return render_template("corpus.html", corpus=dict_mono)

@app.route("/monographie/<mono_id>")
def txt_mono(mono_id):
    """Route that loads a page with monograph text.
    :param mono_id: monograph XML filename.
    :type mono_id: str.
    """
    filename = "../app-ouvriers-deux-mondes/app/static/xml/" + mono_id
    clear_file(filename)
    source_doc = etree.parse(filename)
    xslt_doc = etree.parse("../app-ouvriers-deux-mondes/app/static/xsl/mono_od2m.xsl")
    xslt_transformer = etree.XSLT(xslt_doc)
    output_doc = xslt_transformer(source_doc)
    return render_template("mono.html", template_flask1=output_doc)

@app.route("/search")
def search():
    subtype_tble = [st for st in Subtype.query.all()]
    return render_template("search.html", subtype_tble=subtype_tble)

@app.route("/search/results")
def results():
        return render_template("results.html")

