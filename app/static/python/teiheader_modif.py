#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Author : Jean-Damien Généro
Date : 2021-07-30
Update
Refracting <teiheader> in OD2M files.
"""

import csv
import os
from bs4 import BeautifulSoup


def monographs_dict(local_path, csvfile):
    dict_xml_files = {}
    with open(os.path.join(local_path, csvfile), 'r', encoding='utf-8') as xml_csv:
        file = csv.reader(xml_csv)
        # list_xml_files = [row[2] for row in file if row[2] != 'none']  # xml file name
        for row in file:
            # filename = [num, title, short title, forname1, surname2, quality1, forname2, surname2, quality2, date]
            dict_xml_files[row[2]] = [row[0], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[-1]]
    # del list_xml_files[0] # removing headers + last monograph
    del dict_xml_files['Files XML'], dict_xml_files['none']
    # return list_xml_files
    return dict_xml_files


def new_teiheader(local_path):
    monographs = monographs_dict("/home/genero/Bureau/OD2M/app-ouvriers-deux-mondes/app/static", "csv/id_monographies.csv")
    for filenames in monographs:
        with open(os.path.join(local_path, filenames), 'r', encoding='utf-8') as xml_file:
            soup = BeautifulSoup(xml_file, 'xml')

            # 1. TITLE STATEMENT
            titleStmt = soup.titleStmt
            # 1.1 TITLE
            titleStmt.title['type'] = 'desc'
            titleStmt.title['level'] = 's'
            short_title = soup.new_tag("title", type='short', level='m')
            short_title.string = monographs[filenames][2]
            titleStmt.title.insert_after(short_title)
            full_title = soup.new_tag("title", type='main', level='m', n=monographs[filenames][0])
            full_title.string = monographs[filenames][1]
            titleStmt.title.insert_before(full_title)
            # 1.2 AUTHORS
            author1 = soup.new_tag("author", role="investigator", n="1")
            author1.string = monographs[filenames][3] + " " + monographs[filenames][4]
            last_title = titleStmt.find(type='short')
            last_title.insert_after(author1)
            author2 = soup.new_tag("author", role="investigator", n="2")
            if monographs[filenames][6] != "" and monographs[filenames][7] != "":
                author2.string = monographs[filenames][6] + " " + monographs[filenames][7]
                titleStmt.author.insert_after(author2)
            # 1.3 EDITOR
            editor = soup.new_tag("editor")
            editor.string = "Société internationale des études pratiques d'économie sociale"
            last_author = titleStmt.find(n='2')
            if last_author is not None:
                last_author.insert_after(editor)
            else:
                titleStmt.author.insert_after(editor)

            # EDITION STATEMENT
            soup.encodingDesc.decompose()
            individuals = [soup.respStmt.extract() for resp in soup.find_all("respStmt")]
            edstmt = soup.new_tag("editionStmt")
            titleStmt.insert_after(edstmt)
            ed = soup.new_tag("edition")
            ed.string = "Édition et encodage scientifique de la monographie n°"+ monographs[filenames][0] + ' des Ouvriers des deux mondes, "' + monographs[filenames][1] + '". Elle a été publiée en <date pubbli> à partir d\'une enquête réalisée à <lieu> en <date enquete>.'
            soup.editionStmt.append(ed)
            funder = soup.new_tag("funder")
            funder.string = "Agence nationale de la Recherche"
            soup.editionStmt.append(funder)
            for individual in individuals:
                soup.editionStmt.append(individual)

            # PUBLICATION STATEMENT : publisher + authority + licence
            pubstmt = soup.publicationStmt
            authority = soup.new_tag("authority", source='https://anr.fr/Projet-ANR-16-CE26-0018')
            authority.string = "ANR-16-CE26-0018 – TIME-US – Women’s and men’s remuneration and time budgets in the textile trades in France from the late 17th to the early 20th century"
            pubstmt.append(authority)
            availability = soup.new_tag("availability", status="free")
            licence_tag = soup.new_tag("licence", target='https://github.com/etalab/licence-ouverte/blob/master/open-licence.md')
            licence_tag.string = "Distributed under an Open License 2.0"
            pubstmt.append(availability)
            soup.availability.append(licence_tag)
            soup.publisher.string = "Centre de recherches historiques (UMR 8558), Centre Maurice Halbwachs (UMR 8097), Inria ALMAnaCH"

            # RESPSTMT in TITLESTMT
            respStmt_title = soup.new_tag("respStmt")
            titleStmt.editor.insert_after(respStmt_title)
            resp_title = soup.new_tag("resp")
            resp_title.string = "Fichier XML-TEI encodé de 2019 à 2021"
            titleStmt.respStmt.append(resp_title)
            orgName = soup.new_tag("orgName")
            orgName.string = "programme ANR TIME US"
            titleStmt.respStmt.resp.insert_after(orgName)

            print(soup.prettify())
