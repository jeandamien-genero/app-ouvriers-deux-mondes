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
from lxml import etree


# imports
from .app import app
from .clear_xml import clear_file
# from .constantes import get_section, get_section2, get_txt_from_section, filenames, proprietes_sections,inventories_dict, travaux_sections, industries_sections, par_10_sections, csv_dict


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

"""@app.route("/search")
def search():
    return render_template("search.html", od2m_inventories=inventories_dict)

@app.route("/search/results")
def results():
    proprietes_kw = request.args.get("proprietes", None)
    travaux_kw = request.args.get("travaux", None)
    industries_kw = request.args.get("industries", None)
    par_10_kw = request.args.get("par_10", None)
    dict_proprietes = {}
    dict_travaux = {}
    dict_industries = {}
    dict_par_10 = {}
    if proprietes_kw:
        for st_group in proprietes_sections:
            for st_item in st_group:
                subtype = st_item["subtype"]
                xslt_section = get_txt_from_section(st_item)
                name = re.findall("s\dt\d{,2}_chapt_\d{,2}\\.xml", str(xslt_section))
                xslt_section = re.sub(name[0], csv_dict[name[0]], str(xslt_section))
                xslt_section = str(xslt_section).replace('./app/static/xml/', '')
                dict_proprietes[xslt_section] = subtype
        return render_template("results.html", proprietes_kw=proprietes_kw, dict_proprietes=dict_proprietes)
    elif travaux_kw:
        for work_group in travaux_sections:
            for work_item in work_group:
                subtype = work_item["subtype"]
                xslt_section = get_txt_from_section(work_item)
                name = re.findall("s\dt\d{,2}_chapt_\d{,2}\\.xml", str(xslt_section))
                xslt_section = re.sub(name[0], csv_dict[name[0]], str(xslt_section))
                xslt_section = str(xslt_section).replace('./app/static/xml/', '')
                dict_travaux[xslt_section] = subtype
        return render_template("results.html", travaux_kw=travaux_kw, dict_travaux=dict_travaux)
    elif industries_kw:
        for industries_group in industries_sections:
            for industries_item in industries_group:
                subtype = industries_item["subtype"]
                xslt_section = get_txt_from_section(industries_item)
                name = re.findall("s\dt\d{,2}_chapt_\d{,2}\\.xml", str(xslt_section))
                xslt_section = re.sub(name[0], csv_dict[name[0]], str(xslt_section))
                xslt_section = str(xslt_section).replace('./app/static/xml/', '')
                dict_industries[xslt_section] = subtype
        return render_template("results.html", industries_kw=industries_kw, dict_industries=dict_industries)
    elif par_10_kw:
        for par_10_group in par_10_sections:
            for par_10_item in par_10_group:
                subtype = par_10_item["subtype"]
                xslt_section = get_txt_from_section(par_10_item)
                name = re.findall("s\dt\d{,2}_chapt_\d{,2}\\.xml", str(xslt_section))
                xslt_section = re.sub(name[0], csv_dict[name[0]], str(xslt_section))
                xslt_section = str(xslt_section).replace('./app/static/xml/', '')
                dict_par_10[xslt_section] = subtype
        return render_template("results.html", par_10_kw=par_10_kw, dict_par_10=dict_par_10)
    else:
        return render_template("results.html")"""

