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
import time
import pandas
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
    """
    Getting monographs' places' coordinates.
    :return: None
    """
    start_time = time.time()
    data = pandas.read_csv(make_csv("../csv/geocoder.csv"), index_col="Number", header=0, sep=",")

    def get_latitude(geolocate):
        """
        Getting latitude
        :param geolocate: string with placename region country
        :return: latitude
        :rtype: str
        """
        if hasattr(geolocate, 'latitude') and (geolocate.latitude is not None):
            return geolocate.latitude

    def get_longitude(geolocate):
        """
        Getting longitude.
        :param geolocate: string with placename region country
        :type geolocate: str
        :return: longitude
        :rtype: str
        """
        if hasattr(geolocate, 'longitude') and (geolocate.longitude is not None):
            return geolocate.longitude

    geolocator = Nominatim(user_agent="You", timeout=5)
    data['Localisation'] = data['Settlement'].map(str) + " " + data['Region'].map(str) + " " + data['Country'].map(str)
    data.to_csv("../csv/geocoder.csv")
    geolocate_column = data['Localisation'].apply(geolocator.geocode)
    data['latitude'] = geolocate_column.apply(get_latitude)
    data['longitude'] = geolocate_column.apply(get_longitude)
    data = data.drop(["Settlement", "Region", "Country"], axis=1)
    data.to_csv("../csv/geocoder.csv")
    print("--- %s seconds ---" % (time.time() - start_time))


getting_coordinates()
