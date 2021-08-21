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
    Making a list with monographs places.
    :param file: path to a csv with placename, settlement, country in rows -6, -5, -4.
    :type file: str
    :return: a list made of lists = [placename, settlement, country]
    :rtype: list
    """
    city_list = []
    with open(file) as opening:
        csv_list = csv.reader(opening)
        for line in csv_list:
            city_list.append([line[-7], line[-6], line[-5], line[-4]])
    del city_list[0], city_list[-1]
    return city_list


def make_csv(csvfile):
    """
    Making a csv file with four columns out of a dict where
    {<cityname>: [<settlement>, <departement>, <country>]}
    :param csvfile: path to a csvfile that will be written.
    :type csvfile:str
    :return: a csv file
    :rtype: str
    """
    with open(csvfile, 'w', encoding="utf-8") as openedcsv:
        spamwriter = csv.writer(openedcsv)
        headers = ["PlaceName", "Settlement", "Region", "Country"]
        spamwriter.writerow(headers)
        places = cities("/home/genero/Bureau/OD2M/app-ouvriers-deux-mondes/app/static/csv/id_monographies.csv")
        for place in places:
            row = place[0], place[1], place[2], place[3]
            spamwriter.writerow(row)
    return csvfile


def getting_coordinates() -> None:
    start_time = time.time()
    io = pandas.read_csv(make_csv("/home/genero/Bureau/OD2M/app-ouvriers-deux-mondes/app/static/csv/geocoder.csv"), index_col=None, header=0, sep=",")
    # print(io)

    def get_latitude(x):
        if hasattr(x, 'latitude') and (x.latitude is not None):
            return x.latitude

    def get_longitude(x):
        if hasattr(x, 'longitude') and (x.longitude is not None):
            return x.longitude

    geolocator = Nominatim(user_agent="You", timeout=5)
    io['helper'] = io['Settlement'].map(str) + " " + io['Region'].map(str) + " " + io['Country'].map(str)
    io.to_csv("/home/genero/Bureau/OD2M/app-ouvriers-deux-mondes/app/static/csv/geocoder.csv")
    geolocate_column = io['helper'].apply(geolocator.geocode)

    io['latitude'] = geolocate_column.apply(get_latitude)
    io['longitude'] = geolocate_column.apply(get_longitude)
    io.to_csv("/home/genero/Bureau/OD2M/app-ouvriers-deux-mondes/app/static/csv/geocoder.csv")
    print("--- %s seconds ---" % (time.time() - start_time))


getting_coordinates()
