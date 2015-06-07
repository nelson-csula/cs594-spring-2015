import urllib
import dateutil.parser as dateparser
import re
import urllib2
import xmltodict
import json
import BeautifulSoup as bs
from pprint import pprint
from xml.dom import minidom
from HTMLParser import HTMLParser
from pymongo import MongoClient
import csv


def add_crimes(id, incidentDate, category, stat, statDesc, addressStreet, city, zip, xCoor, yCoor, incidentId, reportDistrict, seq, unitId, unitName, deleted):
    exists = db.crimes.find(
        {
            "incidentId" : incidentId
         }
    )

    if exists.count() == 0:
        result = db.crimes.insert_one(
            {
                "id": id,
                "incidentDate" : incidentDate,
                "category" : category,
                "stat" : stat,
                "statDesc" : statDesc,
                "addressStreet" : addressStreet,
                "city" : city,
                "zip" : zip,
                "xCoor" : xCoor,
                "yCoor" : yCoor,
                "incidentId" : incidentId,
                "reportDistrict" : reportDistrict,
                "seq" : seq,
                "unitId" : unitId,
                "unitName" : unitName,
                "deleted " : deleted
            }
        )
        print incidentId, "happened in", city;

# DB client
mongo = MongoClient()
db = mongo.bigDataTest

# Sheriff's Department Data
# http://shq.lasdnews.net/CrimeStats/CAASS/PART_I_AND_II_CRIMES.csv


print "Loading Sheriff's crimes database..."

csv_path = "2014-PART_I_AND_II_CRIMES.csv"
with open(csv_path, "rb") as csvfile:
    cr = csv.reader(csvfile)

    for row in cr:
        add_crimes(row[11] , row[0]      , row[2]  , row[3], row[4]  , row[5]       , row[7], row[8], row[9], row[10], row[11]   , row[12]       , row[13], row[15], row[16] , row[17]);
