#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
author = Jean-Damien Généro
date = 2020-12-15
"""

# libraries
import csv
import os
from bs4 import BeautifulSoup
from flask import render_template, request
from lxml import etree


# imports
from .app import app
from .clear_xml import clear_file


# functions
def get_filenames():
    """
    Making a list with files paths.
    :return: a dict
    :rtype: list
    """
    file_paths_ls = []
    for file in os.listdir("./app/static/xml"):
        if file.endswith(".xml"):
            file_paths_ls.append(os.path.join("./app/static/xml", file))
    return file_paths_ls


def get_subtypes(files_list):
    proprietes_st = []
    travaux_st = []
    industries_st = []
    par_10_st = []
    subtypes_dict = {}
    subtypes = []
    for item in files_list:
        with open(item) as xml:
            xmlfile = xml.read()
            soup = BeautifulSoup(xmlfile, 'xml')
            subtypes = soup.find_all('div', subtype=True)
            for tag in subtypes:
                if tag["type"] == "proprietes":
                    proprietes_st.append(tag["subtype"])
                elif tag["type"] == "travaux":
                    travaux_st.append(tag["subtype"])
                elif tag["type"] == "industries":
                    industries_st.append(tag["subtype"])
                elif tag["type"] == "par_10":
                    par_10_st.append(tag["subtype"])
    # subtypes_dict["proprietes"] = set(proprietes_st)
    # subtypes_dict["travaux"] = set(travaux_st)
    # subtypes_dict["industries"] = set(industries_st)
    # subtypes_dict["par_10"] = set(par_10_st)
    properties  = list(set(proprietes_st))
    works = list(set(travaux_st))
    industries = list(set(industries_st))
    assets = list(set(par_10_st))
    # return subtypes_dict
    subtypes = [properties, works, industries, assets]
    return subtypes


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
    # with open(filename, 'r', encoding='utf8') as opening:
        # file = opening.read()
        # soup = BeautifulSoup(file, 'xml')
        # del soup.TEI['xmlns']
        # del soup.TEI['xmlns:xi']
        # result = soup.prettify()
    clear_file(filename)
    # with open(filename, 'w', encoding='utf8') as writting:
        # writting.write(result)
    source_doc = etree.parse(filename)
    xslt_doc = etree.parse("../app-ouvriers-deux-mondes/app/static/xsl/mono_od2m.xsl")
    xslt_transformer = etree.XSLT(xslt_doc)
    output_doc = xslt_transformer(source_doc)
    return render_template("mono.html", template_flask1=output_doc)

@app.route("/search")
def search():
    # all_sections = {"Propriétés": "1", "Travaux": "2", "Industries": "3", "Habitation, mobilier et vêtement": "4"}
    all_sections = ["Propriétés", "Travaux", "Industries", "Habitation, mobilier et vêtement"]
    all_subtypes = get_subtypes(get_filenames())
    number = -1
    subdict = {}
    for sublist in all_subtypes:
        number += 1
        for subtype in sublist:
            subdict[subtype] = str(number)
    return render_template("search.html", ls_s=all_sections, subtypes=subdict)

@app.route("/search/results")
def results():
    motclef = request.args.get("keyword", None)
    # il faut définir une variable résult où sera stockée la liste des sections à afficher
    # le keyword est la valeur du xpath (mais il faut deux valeurs ?)
    return render_template("results.html")
