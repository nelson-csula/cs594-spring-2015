# Reference: http://shq.lasdnews.net/CrimeStats/LASDCrimeInfo.html
# Reference: http://shq.lasdnews.net/CrimeStats/CAASS/desc.html

import urllib2
import csv
import datetime
import urllib

def downloadSheriffData(url):
    # Sheriff's Department Data
    # http://shq.lasdnews.net/CrimeStats/CAASS/PART_I_AND_II_CRIMES.csv

    print "Downloading Sheriff's crimes historical file..."

    datafile = urllib.URLopener()
    datafile.retrieve(url, "PART_I_AND_II_CRIMES.csv")

    print "Downloading Sheriff's crimes historical file... DONE!"

urlHistorical = "http://shq.lasdnews.net/CrimeStats/CAASS/2014-PART_I_AND_II_CRIMES.csv"
# urlDaily = 'http://shq.lasdnews.net/CrimeStats/CAASS/PART_I_AND_II_CRIMES.csv';
downloadSheriffData(urlHistorical);