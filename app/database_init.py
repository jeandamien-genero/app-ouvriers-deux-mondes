#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
    author : Jean-Damien Généro
    date : 2021-02-11
"""

import csv
import os
from bs4 import BeautifulSoup

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
    # "./static/csv/id_monographies.csv"
    csv_dict = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        file = csv.reader(f)
        for line in file:
            if line[2] != "none":
                title = [line[0], line[3]]
                csv_dict[line[2]] = title
    del csv_dict['Fichiers XML']
    return csv_dict

def get_subtypes(files_list):
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
    subtypes_dict = {}
    db.drop_all()
    db.create_all()
    types_dict = {"proprietes": "1", "travaux": "2", "industries": "3", "par_10": "4"}
    for label in types_dict:
    	db.session.add(Type(types_dict[label], label))
    db.session.commit()
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
    corpus = filenames_dict("./app/static/csv/id_monographies.csv")
    for line in corpus:
        db.session.add(Monography(corpus[line][0], line, corpus[line][1]))
    inventaires = get_subtypes(files_list)
    number = 0
    for inventaire in inventaires:
        number +=1
        source = inventaire["source"]
        tag_type = inventaire["type"]
        # print("\n{}\n>>>>>>>>>>>>>>>>>>>>>>>>>>> {} ####### {} ############## {} ########################\n\n".format(number, inventaire, corpus[source][0], types_dict[inventaire["type"]]))
        db.session.add(Inventory(number, str(inventaire), corpus[source][0], types_dict[tag_type], new_subtypes_dict[inventaire["subtype"]]))
    db.session.commit()

