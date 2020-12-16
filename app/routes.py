#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
author = Jean-Damien Généro
date = 2020-12-15
"""


# libraries
import csv
from bs4 import BeautifulSoup
from flask import render_template
from lxml import etree


# imports
from .app import app


# routes
@app.route("/")
def home():
    """Route that loads the home page.
    """
    return render_template("home.html")

@app.route("/monographies")
def monographies():
    """Route that loads a page with the monographies list out of a CSV.
    Works with a dictionary where monographies' titles are keys and XML
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
    :param mono_id: str.
    """
    filename = "../app-ouvriers-deux-mondes/app/static/xml/" + mono_id
    with open(filename, 'r', encoding='utf8') as opening:
        file = opening.read()
        soup = BeautifulSoup(file, 'xml')
        del soup.TEI['xmlns']
        del soup.TEI['xmlns:xi']
        result = soup.prettify()
    with open(filename, 'w', encoding='utf8') as writting:
        writting.write(result)
    source_doc = etree.parse(filename)
    xslt_doc = etree.parse("../app-ouvriers-deux-mondes/app/static/xsl/mono_od2m.xsl")
    xslt_transformer = etree.XSLT(xslt_doc)
    output_doc = xslt_transformer(source_doc)
    return render_template("mono.html", template_flask1=output_doc)
