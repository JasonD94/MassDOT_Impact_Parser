# MassDOT_Impact_Parser
A Python script to parse MassDOT Impact Data files, as well as combine various years into one easy to use CSV

## Requires:
Library: [pandas](https://pandas.pydata.org/)

Follow the [Getting started](https://pandas.pydata.org/getting_started.html)
instructions on the pandas webpage for help setting up pandas on your machine

Plus (these _should_ be standard to Python 3.7.3): glob, time, os, sys, logging

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
