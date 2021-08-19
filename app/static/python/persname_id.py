#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Author : Jean-Damien Généro
Affiliation : French National Center for Scientific Research (CNRS)
Assigned at the Centre de recherches historiques (CRH, UMR 8558)
Date : 2021-07-28
Update : 2021-08-19
"""


import csv
import os
from bs4 import BeautifulSoup


def monographs(fileslist):
    """
    Making a dict with monographs.
    :param fileslist: csv with monographs list, where column 1 is monographs' Ids and column 2 monographs' filenames.
    :type fileslist: str
    :return: a dict where {filename: id, ...}
    :rtype: dict
    """
    with open(fileslist) as opening:
        csv_list = csv.reader(opening)
        monographs = {}
        for line in csv_list:
            monographs[line[2]] = line[1]
    del monographs["Fichiers XML"], monographs["none"]
    return monographs


def investigators() -> None:
    """
    Adding persName id. ID = "ID-" + monograph's id + "E" + persName index order.
    """
    monographs_dict = monographs("../csv/id_monographies.csv")
    for monograph in monographs_dict:
        path = os.path.join("../xml", monograph)
        with open(path, 'r', encoding='utf-8') as opened_xml:
            soup = BeautifulSoup(opened_xml, 'xml')
            text = soup.findAll("div", {"n": "002", "type": "section"})
            for tag in text:
                persnames = tag.findAll("persName")
                counter = 0
                for persname in persnames:
                    counter +=1
                    persname["xml:id"] = "ID-" + monographs[monograph] + "E" + str(counter)
            result = soup.prettify()
        with open(path, 'w', encoding='utf-8') as writting:
            writting.write(result)
            print("{} ----> Done !".format(path))
