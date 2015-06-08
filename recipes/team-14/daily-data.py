import urllib2
from pymongo import MongoClient
import csv
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

def add_crimes(id, incidentDate, category, stat, statDesc, addressStreet, city, zip, xCoor, yCoor, incidentId, reportDistrict, seq, unitId, unitName, deleted):
    exists = db.crimes.find(
        {
            "id" : id
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
        print city

def loadSheriffsDatabase():
    # Sheriff's Department Data
    # http://shq.lasdnews.net/CrimeStats/CAASS/PART_I_AND_II_CRIMES.csv

    print "Loading Sheriff's crimes database..."
    print datetime.datetime.utcnow()
    url = 'http://shq.lasdnews.net/CrimeStats/CAASS/PART_I_AND_II_CRIMES.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)

    for row in cr:
        add_crimes(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15])

    print "Sheriff's crimes database load complete."

###############################################################
## Data Acquisition Main()

debug = 0

# DB client
mongo = MongoClient()
db = mongo.bigDataTest

#loadSources()

# Define scheduler
scheduler = BlockingScheduler()
#scheduler = BackgroundScheduler()

print "Adding Sheriffs database scheduled job executing every 12  hours..."
scheduler.add_job(loadSheriffsDatabase, 'interval', hours=12, id='load_sheriff')

loadSheriffsDatabase()

print "Starting scheduler..."
print datetime.datetime.utcnow()
scheduler.start()


#print "Removing Load Sources job..."
#scheduler.remove_job('load_sources')

#print "Removing Sheriff's database scheduled job..."
#scheduler.remove_job('load_sheriff')
