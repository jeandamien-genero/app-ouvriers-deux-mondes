#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Author : Jean-Damien Généro
Affiliation : French National Center for Scientific Research (CNRS)
Assigned at the Centre de recherches historiques (CRH, UMR 8558)
Date : 2021-08-19
Update : 2021-08-21
"""

import csv
import pandas
import time
from geopy.geocoders import Nominatim


def cities(file):
    """
    Making a list with monographs informations and places.
    :param file: path to a csv with placename, settlement, country in rows -6, -5, -4.
    :type file: str
    :return: a list made of lists >>
    city_list = [[number, title, author(s), filename, place, settlement, region, country, publication date], [...]]
    :rtype: list
    """
    city_list = []
    with open(file) as opening:
        csv_list = csv.reader(opening)
        for line in csv_list:
            if line[8] != "":  # two authors
                author = line[5] + " " + line[6] + " et " + line[8] + " " + line[9]
            else:  # one author
                author = line[5] + " " + line[6]
            city_list.append([line[0], line[3], author, line[2], line[-7], line[-6], line[-5], line[-4], line[-2]])
    del city_list[0], city_list[-1]
    return city_list


def make_csv(csvfile):
    """
    Making a csv file with four columns out of a list made with cities() function.
    :param csvfile: path to a csvfile that will be written.
    :type csvfile:str
    :return: a csv file
    :rtype: str
    """
    with open(csvfile, 'w', encoding="utf-8") as openedcsv:
        spamwriter = csv.writer(openedcsv)
        headers = ["Number", "Monograph", "Author(s)", "File", "PlaceName", "Settlement", "Region", "Country", "Date"]
        spamwriter.writerow(headers)
        places = cities("../csv/id_monographies.csv")
        for place in places:
            row = place[0], place[1], place[2], place[3], place[4], place[5], place[6], place[7], place[8]
            spamwriter.writerow(row)
    return csvfile


def getting_coordinates() -> None:
    start_time = time.time()
    io = pandas.read_csv(make_csv("../csv/geocoder.csv"), index_col="Number", header=0, sep=",")

    def get_latitude(x):
        if hasattr(x, 'latitude') and (x.latitude is not None):
            return x.latitude

    def get_longitude(x):
        if hasattr(x, 'longitude') and (x.longitude is not None):
            return x.longitude

    geolocator = Nominatim(user_agent="You", timeout=5)
    io['Localisation'] = io['Settlement'].map(str) + " " + io['Region'].map(str) + " " + io['Country'].map(str)
    io.to_csv("../csv/geocoder.csv")
    geolocate_column = io['Localisation'].apply(geolocator.geocode)
    io['latitude'] = geolocate_column.apply(get_latitude)
    io['longitude'] = geolocate_column.apply(get_longitude)
    io = io.drop(["Settlement", "Region", "Country"], axis=1)
    io.to_csv("../csv/geocoder.csv")
    print("--- %s seconds ---" % (time.time() - start_time))


getting_coordinates()
