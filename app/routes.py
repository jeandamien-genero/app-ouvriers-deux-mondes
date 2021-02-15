#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
author = Jean-Damien Généro
date = 2020-12-15 - 2021-02-15
"""

# libraries
import csv
import os
import re
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc
from lxml import etree

#imports
from .app import app
from .clear_xml import clear_file
from .database_init import get_filenames, tables_init
from .modeles.data import Type, Subtype, Monography, Inventory


# database inception
tables_init(get_filenames("./app/static/xml", ".xml"))


# routes
@app.route("/")
def home():
    """Loading the home page.
    """
    return render_template("home.html")

@app.route("/monographies")
def monographies():
    """Loading a page with the monographs list out of a CSV.
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
    """Loading a page with monograph text.
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
    """Loading the search page.
    """
    subtype_tble = [st for st in Subtype.query.all()]
    mono = [mono for mono in Monography.query.all()]
    inv = [inventaire for inventaire in Inventory.query.all()]
    return render_template("search.html", subtype_tble=subtype_tble, mono=mono, inv=inv)

@app.route("/search/results")
def results():
    """Loading the results page.
    """
    proprietes_kw = request.args.get("proprietes", None)
    travaux_kw = request.args.get("travaux", None)
    industries_kw = request.args.get("industries", None)
    par_10_kw = request.args.get("par_10", None)
    result_prop = []
    if proprietes_kw:
        result_prop = Inventory.query.filter(Inventory.subtype_inv_fk == proprietes_kw).order_by(Inventory.mono_inv_fk.asc())
        return render_template("results.html", proprietes_kw=proprietes_kw, result_prop=result_prop)
    if travaux_kw:
        result_trav = Inventory.query.filter(Inventory.subtype_inv_fk == travaux_kw).order_by(Inventory.mono_inv_fk.asc())
        return render_template("results.html", travaux_kw=travaux_kw, result_trav=result_trav)
    if industries_kw:
        result_indus = Inventory.query.filter(Inventory.subtype_inv_fk == industries_kw).order_by(Inventory.mono_inv_fk.asc())
        return render_template("results.html", industries_kw=industries_kw, result_indus=result_indus)
    if par_10_kw:
        result_par_10 = Inventory.query.filter(Inventory.subtype_inv_fk == par_10_kw).order_by(Inventory.mono_inv_fk.asc())
        return render_template("results.html", par_10_kw=par_10_kw, result_par_10=result_par_10)
    else:
        return render_template("results.html")

