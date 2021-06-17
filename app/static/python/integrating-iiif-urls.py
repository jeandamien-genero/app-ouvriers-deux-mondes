#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Author : Jean-Damien Généro
Affiliation : French National Center for Scientific Research (CNRS)
Assigned at the Centre de recherches historiques (CRH, UMR 8558)
Date : 2021-06-17
Update :
Two functions that make Gallica IIIF urls and adding them in an XML file's //facsimile/graphic/@url.
Try it out with this param :
substituting_path_by_url("../xml/s3t3_chapt_3.xml", make_gallica_iiif_url("ark:/12148/bpt6k6154186x", 77, 167))
"""

import re
from bs4 import BeautifulSoup


def make_gallica_iiif_url(ark, page_number, file_number):
    """
    Making Gallica IIIF URL with first page number and firt IIIF file number.
    :param ark: Gallica ark
    :type ark: str
    :param page_number: first page number
    :type page_number: int
    :param file_number: first iiif file number
    :type file_number: int
    :return: list with all urls.
    :rtype: list
    """
    urls = []
    url = "https://gallica.bnf.fr/iiif/"
    param = "/full/full/0/native.jpg"
    page_number -= 1
    file_number -= 1
    while page_number != 109:
        page_number += 1
        file_number += 1
        iiif_url = url + ark + "/f" + str(file_number) + param
        urls.append(iiif_url)
        # print("Page n°{} ----> {}".format(page_number, iiif_url))
    return urls


def substituting_path_by_url(file, url_list) -> None:
    """
    Substituting file path by Gallica IIIF url in //facsimile/graphic/@url.
    :param file: path to the XML file
    :type file: str
    :param url_list: list of Gallica IIIF url
    :type url_list: list
    """
    with open(file, 'r', encoding='utf-8') as opening:
        xml = opening.read()
        soup = BeautifulSoup(xml, 'xml')
        facsimile = soup.find_all('facsimile')
        dict = {facsimile[url]: url_list[url] for url in range(len(facsimile))}
        for tag in dict:
            old_value = tag.graphic["url"]
            tag.graphic["url"] = dict[tag]
            soup = re.sub(old_value, tag.graphic["url"], str(soup))
        result = BeautifulSoup(soup, 'xml').prettify()
    with open(file, 'w', encoding='utf-8') as writting:
        writting.write(result)
        print("{} IIIF url integrated in {}".format(len(url_list), file))
