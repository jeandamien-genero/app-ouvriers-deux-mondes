#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Author : Jean-Damien Généro
Affiliation : French National Center for Scientific Research (CNRS)
Assigned at the Centre de recherches historiques (CRH, UMR 8558)
Date : 2021-03-31
Update : 2021-07-29
"""

import csv
import os
import re
from lxml import etree


def xtract_txt(local_path) -> None:
    """
    Extracting plain text from monographs' xmlfiles.
    :param local_path: path to the repository containing monographs' xmlfiles (= static).
    :type local_path: str
    """
    xslt_root = etree.XML(f"""<xsl:stylesheet version="1.0"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:x="http://www.tei-c.org/ns/1.0">
        <xsl:output method="text"/>
        <xsl:strip-space elements="*"/>
        <xsl:template match="x:text/x:body//text()">
            <xsl:value-of select="."/>
        </xsl:template>
        <xsl:template match="text()"/>
    </xsl:stylesheet>""")
    xslt_transformer = etree.XSLT(xslt_root)
    with open(os.path.join(local_path, "csv/id_monographies.csv"), 'r', encoding='utf-8') as xml_csv:
        file = csv.reader(xml_csv)
        list_xml_files = [row[2] for row in file if row[1] != 'none']
    del list_xml_files[0], list_xml_files[-1]
    for filenames in list_xml_files:
        with open(os.path.join(local_path, 'xml/' + filenames), 'r') as xml_file:
            reading = xml_file.read()
            reading = re.sub(r'(<TEI xml:id="ID-\d+[a-c]" xml:lang="fr")>', '\\1 xmlns="http://www.tei-c.org/ns/1.0">', reading)
            result = reading
        with open(os.path.join(local_path, 'xml/' + filenames), 'w') as writting:
            writting.write(result)
        with open(os.path.join(local_path, 'xml/' + filenames), 'r') as xml_file:
            source_doc = etree.parse(xml_file)
            output_doc = xslt_transformer(source_doc)
        with open(os.path.join(local_path, 'txt/' + filenames.replace('.xml', '.txt')), 'w') as txt_file:
            output_doc = re.sub(r' +\n', r'', str(output_doc))
            output_doc = re.sub(r'      +', r'', str(output_doc))
            txt_file.write(str(output_doc))
            print("{} -----> Done !".format(filenames.replace('.xml', '.txt')))


xtract_txt("../")
