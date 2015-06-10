# Crime Against Crime

**Problem:** Do specific types of crimes predict other types of crimes in Los Angeles?
**Solution:** use python numpy and bokeh library to visually represent relationships between crime types

## Summary
The following files download, parse, and visualize the correlation between types of crimes provided by the Los Angeles Sheriff's Department.

## Details
- `download_historical.py`: 
  - downloads historical crime data (2014 yearly data) file
- `daily_data.py`: 
  - downloads daily crime data
  - inserts it into mongdb 
  - sets up a scheduler to repeat this process daily
- `historical_crime.py`: 
  - reads the historical crime data file downloaded and inserts the data into mongo db
- `calc_and_plot.py`: 
  - takes the data inserted into mongodb using `daily_data.py` and/or `historical_crime.py`, calculates the correlation between types of crimes, and plots the result.
 

## References:
- http://bokeh.pydata.org/en/latest/docs/quickstart.html
- http://stackoverflow.com/questions/22886331/numpy-correlation-coefficient-and-related-statistical-functions-dont-give-sam
- http://shq.lasdnews.net/CrimeStats/CAASS/desc.html
- http://shq.lasdnews.net/CrimeStats/LASDCrimeInfo.html
