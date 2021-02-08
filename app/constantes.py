#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
author = Jean-Damien Généro
date = 2021-02-08
"""

import csv
import os
import re
from bs4 import BeautifulSoup
from lxml import etree

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


def get_types(files_list):
	"""
	problème = les @type sont dans le mauvais ordre : par_10 proprietes travaux industries
	"""
	types_ls = []
	for item in files_list:
		with open(item) as xml:
			xmlfile = xml.read()
			soup = BeautifulSoup(xmlfile, 'xml')
			types = soup.find_all('div', type=True, subtype=True)
			for tag in types:
				types_ls.append(tag["type"])
	return(list(set(types_ls)))


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
    properties  = list(set(proprietes_st))
    works = list(set(travaux_st))
    industries = list(set(industries_st))
    assets = list(set(par_10_st))
    subtypes = [properties, works, industries, assets]
    return subtypes


def get_section(list_of_files, section_type, section_subtype):
    """
    Function that find a specific section in each monographs and make a dict
    with monography's filenames key and the section as its value.
    :return: a dict
    :rtype: dict
    """
    ls_sections = {}
    for item in list_of_files:
        with open(item) as xml:
            xmlfile = xml.read()
            soup = BeautifulSoup(xmlfile, 'xml')
        sections = soup.find_all('div', type=section_type, subtype=section_subtype)
        for tag in sections:
        	tag["source"] = item.replace("./static/xml/", "")
        	ls_sections[item] = tag
    return ls_sections

def get_section2(list_of_files, section_type, section_subtype):
	ls_sections2 = []
	for item in list_of_files:
		with open(item) as xml:
			xmlfile = xml.read()
			soup = BeautifulSoup(xmlfile, 'xml')
			sections = soup.find_all('div', type=section_type, subtype=section_subtype)
			for tag in sections:
				tag["source"] = item.replace("./static/xml/", "")
				ls_sections2.append(tag)
	return ls_sections2



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
        <p><xsl:value-of select="./@source"/></p>
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


proprietes_sections = []
travaux_sections = []
industries_sections = []
par_10_sections = []
csv_dict = {}

# with open("./static/csv/id_monographies.csv", 'r', encoding='utf-8') as f:
with open("./app/static/csv/id_monographies.csv", 'r', encoding='utf-8') as f:
    file = csv.reader(f)
    for line in file:
        if line[2] != "none":
            title = "{} (n°{})".format(line[3], line[0])
            csv_dict[line[2]] = title


filenames = get_filenames("./app/static/xml", ".xml")
# filenames = get_filenames("./static/xml", ".xml")

types = ["proprietes", "travaux", "industries", "par_10"]

subtypes = get_subtypes(filenames)

inventories_dict = {types[item]: subtypes[item] for item in range(len(types))}


for st in inventories_dict["proprietes"]:
	st = get_section2(filenames, "proprietes", st)
	proprietes_sections.append(st)


for st in inventories_dict["travaux"]:
	st = get_section2(filenames, "travaux", st)
	travaux_sections.append(st)

for st in inventories_dict["industries"]:
	st = get_section2(filenames, "industries", st)
	industries_sections.append(st)

for st in inventories_dict["par_10"]:
	st = get_section2(filenames, "par_10", st)
	par_10_sections.append(st)
