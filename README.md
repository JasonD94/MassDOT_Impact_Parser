# MassDOT_Impact_Parser
A Python script to parse [MassDOT Impact](https://massdot-impact-crashes-vhb.opendata.arcgis.com/) 
Data files, as well as combine various years into one easy to use CSV

## Requires:
Library: [pandas](https://pandas.pydata.org/)

Follow the [Getting started](https://pandas.pydata.org/getting_started.html)
instructions on the pandas webpage for help setting up pandas on your machine

Plus (these _should_ be standard to Python 3.7.3): glob, time, os, sys, logging

You'll also need data from the [MassDOT Impact](https://massdot-impact-crashes-vhb.opendata.arcgis.com/)
system, also called the MassDOT Crash Open Data Portal. Each year's worth of data
is about ~150MB. You can search the MassDOT system with queries like:

```
2010 crashes
```

This would display a map with all the crashes across Massachusetts in 2010.

For testing this script, I downloaded data from 2010 to 2021 and confirmed that
the script could handle merging ~2GB worth of CSV files and handle filtering that
much data down to the City/Roadway level. It appears to work quite well on my machine,
which is an older i7 with 24GB. Do note that you'll need a solid amount of RAM,
at least 2GB+ but ideally I'd guess 8GB or 16GB to run this on multiple years worth
of data. If you experience issues running this script, either reduce the number
of CSV files you're parsing/filtering on, or try to get access to a machine with
more RAM. There's not much I can do about the size of this data except hopefully
over time reduce the number of crashes happening in MA... each year has over
_100,000 crashes_ which is just insane.

## Example usage

Parse the Mass DOT data for the City of [Somerville MA](https://en.wikipedia.org/wiki/Somerville,_Massachusetts) 
and then down to [Highland Ave](https://www.google.com/search?q=highland+ave+somerville)
```
	python massDotParser.py csv "Somerville" "Highland Ave"
```

Example run:
```
	$ python massDotParser.py csv "Somerville" "Highland Ave"
	Starting massDotParser.py
	filePath: csv
	city: Somerville
	roadway: Highland Ave
	******************************************************************************
	Number of Somerville rows: 9357, Number of Somerville columns: 119
	Number of Highland Ave rows: 396, Number of Highland Ave columns: 119
	Number of Roadways in Cambridge: 2477
	Number of crashes in Somerville on Highland Ave: 396
	Execution time in seconds: 47.64 seconds
```

Parse the Mass DOT data for the City of [Cambridge, MA](https://en.wikipedia.org/wiki/Cambridge,_Massachusetts) and then down to [Memorial Drive](https://www.google.com/search?q=memorial+drive+cambridge+ma)
```
	python massDotParser.py csv "Cambridge" "Memorial Drive"
```

Example run:
```
	$ python massDotParser.py csv "Cambridge" "Memorial Drive"
	Starting massDotParser.py
	filePath: csv
	city: Cambridge
	roadway: Memorial Drive
	******************************************************************************
	Number of Cambridge rows: 19169, Number of Cambridge columns: 120
	Number of Memorial Drive rows: 1359, Number of Memorial Drive columns: 120
	Number of Roadways in Cambridge: 4793
	Number of crashes in Cambridge on Memorial Drive: 1359
	Execution time in seconds: 136.75 seconds
```
