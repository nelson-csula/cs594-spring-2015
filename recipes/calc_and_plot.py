# Reference: http://bokeh.pydata.org/en/latest/docs/quickstart.html
# Reference:  http://stackoverflow.com/questions/22886331/numpy-correlation-coefficient-and-related-statistical-functions-dont-give-sam
# use: pip install bokeh
###########################

import time

from bokeh.charts import BoxPlot, output_file, show, Bar
from bokeh.plotting import figure, show, output_file, vplot, figure, output_file, show
import numpy as np
from pymongo import MongoClient
import operator;

mongo = MongoClient()
db = mongo.bigDataTest

def f7(seq):
    seen = set();
    seen_add = seen.add;
    return [ x for x in seq if not (x in seen or seen_add(x))];

# fetch data from mongodb
# for the given crime, returns { date : count }
def getCrimeCountByDate( crime ):
    computed = [ "$parsedDate",0,10  ];

    pipeline = [
        # Lets find our records
        {"$match":{"category":{"$eq": crime} }, },

        # Now lets group on the name counting how many grouped documents we have
        {
            "$group": {
                "_id": {
                    "$substr": [ "$parsedDate",0,10  ]
                }
                , "sum":{"$sum":1}
            }
         },

        {
            "$sort": { "_id": 1  }
        }
    ]

    results = db.crimes.aggregate( pipeline );
    return results;

# objects in the form { date: count }
# returns result[key] = [ date1, date2, date3, ... daten ]
# and     result[value= [ count1, count2, count3, ... countn ]
# also converts each date(i) value into an epoch
def getAsArrays(objects, key, value):
    dateList = [];
    valueList = [];

    for object in objects:
        k = object[key];
        v = object[value];
        # print k , v;
        date_time = k;
        pattern = '%Y-%m-%d';
        if len(str(date_time)) >= 10:
            epoch = int(time.mktime(time.strptime(date_time, pattern))) * 1000;
            dateList.append(epoch);
            valueList.append(v);

    result = { };
    result[key] = dateList;
    result[value] = valueList;
    return result;

# some crimes may occur on one day but not another
# this function returns the list of unique dates for all crime types, result["date"]
# also returns the counts for each crime in result[crime1], result[crime2], etc such that
# days without a specific crime now have a zero value.
# this way, all crimes are on the same date scale.
def combine(listForData, key, value):
    tmp = {};
    result = {};

    allDates = [];
    for crime in listForData:
        tmp[crime] = {};
        result[crime] = [];
        countByDate = getCrimeCountByDate(crime);
        arrayObject = getAsArrays(countByDate, key, value);
        tmp[crime][key] = arrayObject[key]; # date array
        tmp[crime][value] = arrayObject[value]; # value array

        # combine dates into one giant list
        tmpDates = allDates + tmp[crime][key];
        allDates = tmpDates;

    # dedup and sort
    uniqueDates = sorted(f7(allDates));

    result["date"] = uniqueDates;
    for idxUniqueDate, u in enumerate(uniqueDates):
        # print u;
        for crime in listForData:
            v = 0;
            if u in tmp[crime][key]:
                dateIndex = tmp[crime][key].index(u);
                v = tmp[crime][value][dateIndex];
            result[crime].append(v);

    return result;


cats = [ "ARSON", "CRIMINAL HOMICIDE", "AGGRAVATED ASSAULT", "BURGLARY", "DISORDERLY CONDUCT", "DRUNK / ALCOHOL / DRUGS", "DRUNK DRIVING VEHICLE / BOAT", "FELONIES", "FORCIBLE RAPE", "NARCOTICS"];
result = combine( cats, "_id", "sum");

# timeseries3( cats, result );


c1 = 0;
c2 = 0;
item = 0;
correlations = {};
correlations_detail = {};
polyfit_detail = {};

print "*****************";
print " Checking for... "
print "*****************";

# correlation between all crime combinations
for i in result.keys():
    c1 = c1 + 1;
    for j in result.keys():
        c2 = c2 + 1;
        item = item + 1;
        if i != j:
            print "  correlation between", i, "and", j;

            x = result[i];
            y = result[j];

            cc = np.corrcoef(x,y);

            correlations[item] = cc[0][1];
            correlations_detail[item] = {};
            correlations_detail[item][i] = x;
            correlations_detail[item][j] = y;

            polyfit_detail[item] = np.polyfit(result[i],result[j],1);

# sort the dictionary in reverse (highest correlation goes first)
correlations_sorted = sorted(correlations.items(), key=operator.itemgetter(1), reverse=True);

# we could have a large number of plots, so we limit the results with 'plots_to_include'
plots_to_include = 7;

counter = 0;
for v in correlations_sorted:
    counter = counter + 1;
    # correlations are symmetric for crimes (A,B) and (B,A) and they are sorted
    # so we only process even items in the correlations_detail
    if counter % 2 == 0:
        k = v[0];
        keys = correlations_detail[k].keys();
        c = v[1] * 100;

        # print crime pair, correlation percentage and expected filename
        print keys[0], "and", keys[1], "has " + str(c) + "% correlation for regression-" + str(counter) + ".html";

        # get detail and plot
        regression = polyfit_detail[k];

        x = correlations_detail[k][keys[0]];
        y = correlations_detail[k][keys[1]];
        max_x = max(x);

        r_x, r_y = zip(*((i, i*regression[0] + regression[1]) for i in range(max_x)));


        u = figure(tools = "pan,wheel_zoom,box_zoom,reset,save", x_axis_label=keys[0], y_axis_label=keys[1]);
        u.line(r_x, r_y, color="red");

        u.scatter(x, y, marker="square", color="blue")

        output_file("regression-" + str(counter) + ".html");
        show(u);

    if counter == plots_to_include * 2:
        break;

