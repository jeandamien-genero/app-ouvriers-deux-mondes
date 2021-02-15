#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
    author : Jean-Damien Généro
    date : 2021-02-11
"""

import csv
import os
from bs4 import BeautifulSoup
from lxml import etree

from .app import db
from .modeles.data import Type, Subtype, Monography, Inventory

def get_filenames(path, extension):
	"""
    Making a list with files paths.
    :param path: path to a directory
    :type path: str
    :param extension: file extension
    :type extension: str
    :return: a dict
    :rtype: list
    """
	file_paths_ls = []
	for file in os.listdir(path):
		if file.endswith(extension):
			file_paths_ls.append(os.path.join(path, file))
	return file_paths_ls


def filenames_dict(csv_path):
    """Making a dict where XML filename = monograph's number, monograph's title.
    """
    csv_dict = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        file = csv.reader(f)
        for line in file:
            if line[2] != "none":
                title = [line[0], line[3]]
                csv_dict[line[2]] = title
    del csv_dict['Fichiers XML']
    return csv_dict

def get_txt_from_section(xml):
    """
    Transforming with an XSLT stylesheet a monography's section as text.
    :return: str
    """
    xslt_root = etree.XML(f"""<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:xi="http://www.w3.org/2001/XInclude" exclude-result-prefixes="xs tei xi" version="1.0">
    <xsl:output omit-xml-declaration="yes" method="html" indent="yes" encoding="UTF-8"/>
    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="div">
        <div>
        <xsl:apply-templates/>
        </div>
    </xsl:template>
    <xsl:template match="p">
        <xsl:element name="p"><xsl:value-of select="normalize-space(.)"/></xsl:element>
    </xsl:template>
    </xsl:stylesheet>""")
    transform = etree.XSLT(xslt_root)
    tei = f"""<TEI>{xml}</TEI>"""
    tree = etree.fromstring(tei)
    result_tree = transform(tree)
    return result_tree

def get_subtypes(files_list):
    """Getting all @subtype from XML files.
    """
    subtypes = []
    for item in files_list:
        with open(item) as xml:
            xmlfile = xml.read()
            soup = BeautifulSoup(xmlfile, 'xml')
            subtype = soup.find_all('div', subtype=True)
        for tag in subtype:
            tag["source"] = item.replace("./app/static/xml/", "")
            subtypes.append(tag)
    return subtypes


def tables_init(files_list):
    """Initialization of the database
    """
    db.drop_all()
    db.create_all()
    # table >> TYPE
    subtypes_dict = {}
    types_dict = {"proprietes": "1", "travaux": "2", "industries": "3", "par_10": "4"}
    for label in types_dict:
    	db.session.add(Type(types_dict[label], label))
    db.session.commit()
    # table >> SUBTYPE
    for item in files_list:
        with open(item) as xml:
            xmlfile = xml.read()
            soup = BeautifulSoup(xmlfile, 'xml')
            subtypes = soup.find_all('div', subtype=True)
            for tag in subtypes:
                if tag["type"] == "proprietes":
                    subtypes_dict[tag["subtype"]] = "1"
                elif tag["type"] == "travaux":
                    subtypes_dict[tag["subtype"]] = "2"
                elif tag["type"] == "industries":
                    subtypes_dict[tag["subtype"]] = "3"
                elif tag["type"] == "par_10":
                    subtypes_dict[tag["subtype"]] = "4"
    number = 0
    new_subtypes_dict = {}
    for entry in subtypes_dict:
        number +=1
        new_subtypes_dict[entry] = number
        db.session.add(Subtype(number, entry, subtypes_dict[entry]))
    db.session.commit()
    # table >> MONOGRAPHY
    corpus = filenames_dict("./app/static/csv/id_monographies.csv")
    for line in corpus:
        db.session.add(Monography(corpus[line][0], line, corpus[line][1]))
    # table >> INVENTORY
    inventaires = get_subtypes(files_list)
    number = 0
    for inventaire in inventaires:
        number +=1
        source = inventaire["source"]
        tag_type = inventaire["type"]
        text = str(inventaire)
        db.session.add(Inventory(number, text, corpus[source][0], types_dict[tag_type], new_subtypes_dict[inventaire["subtype"]]))
    db.session.commit()

