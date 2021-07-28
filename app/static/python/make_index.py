#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Author : Jean-Damien Généro
Date : 2020-06-15
Update :
"""

import csv
from bs4 import BeautifulSoup


def make_index(table, xml_file):
    """Function that writes an index in a xml file out of a csv file.
        :param table: path to a csv file
        :type table: str
        :param xml_file: path to an xml file where the index will be written.
        :type xml_file: str
    """
    with open(table, 'r', encoding='utf8') as new_file:
        reader = csv.DictReader(new_file)
        list1 = []
        for row in reader:
            header = list(row.keys())
            id_mono = row[header[0]]
            id_indiv = row[header[1]]
            title = row[header[3]]
            nom = row[header[9]]
            prenom = row[header[8]]
            age = row[header[13]]
            birth_date = row[header[14]]
            bith_place = row[header[12]]
            occupation = row[header[16]]
            state = row[header[10]]
            wedding = row[header[11]]
            wedding_date = row[header[15]]
            ref_date = row[header[6]]
            index_entry = f"""<person xml:id="ID-{id_indiv}">
            <persName><forename>{prenom}</forename><surname>{nom}</surname></persName>
            <birth><date>{birth_date}</date><name type="birth_place">{bith_place}</name></birth>
            <age>{age}</age>
            <state><p>{state}</p></state>
            <occupation>{occupation}</occupation>
            <event type="wedding"><desc>{wedding}{wedding_date}</desc></event>
            <note><p>Date de référence pour les calculs : {ref_date}.</p><p>Monographie : {title} ({id_mono}).</p></note>
            </person>"""
            list1.append(index_entry)
        ingredients = ''.join(list1)
        tree = f"""<TEI xmlns='http://www.tei-c.org/ns/1.0'>
                    <teiHeader>
                    <fileDesc>
                    <titleStmt>
                        <title>Index prosopographique des individus enquêtés dans Les Ouvriers des deux mondes</title>
                        <respStmt>
                            <resp>originellement préparé par</resp><name>Jean-Damien Généro</name>
                        </respStmt>
                        <respStmt>
                            <resp>supervisé par</resp><name>Alix Chagué</name>
                        </respStmt>
                        <respStmt>
                            <resp>à partir d'un fichier csv constitué par</resp><name>Stéphane Baciocchi</name>
                        </respStmt>
                    </titleStmt>
                    <publicationStmt>
                        <publisher>projet ANR Time Us</publisher>
                        <date when='2020'/><pubPlace>Paris, France</pubPlace>
                    </publicationStmt>
                    <sourceDesc>
                        <p>Les Ouvriers des Deux Mondes sont des recueils d'enquêtes sociologiques publiées pendant la deuxième moitié du XIXe siècle. Ces enquêtes ont été rassemblées sous la forme de 3 séries de plusieurs volumes. Accès aux fichiers images sources : http://timeusage.paris.inria.fr/mediawiki/index.php/Aperçu_des_états#Les_Ouvriers_des_Mondes</p>
                    </sourceDesc>
                    </fileDesc>
                    </teiHeader>
                    <text>
                    <body>
                    <listPerson>
                    {ingredients}
                    </listPerson>
                    </body>
                    </text>
                    </TEI>"""
        soup = BeautifulSoup(tree, 'xml')
        soup = soup.prettify()
        # BS automatically replaces "xmlns=" by "xmlns:=",
        # so we put it back to its first value
        final_result = soup.replace('xmlns:', 'xmlns')
        with open(xml_file, 'w', encoding='utf8') as xml_index:
            xml_index.write(final_result)
