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

## How to get all this data?

Well, MassDOT sure doesn't make it easy. It appears their datasets go all the way
back to circa _2002_, so you can search the MassDOT IMPACT system for the following
terms to get datasets:

"2002 crashes", "2003 crashes", ..., "2020 crashes", "2021 crashes"

Note that MassDOT warns the following on their webpage:

> In addition, any crash records or data provided for the years 2017 and later 
> are subject to change at any time and are not to be considered up-to-date or 
> complete. As such, open years’ of crash data are for informational purposes only 
> and should not be used for analysis.

Crash data can be downloaded in CSV, KML, Shapefile, GeoJSON and file Geodatabase
formats. This script works off of the CSV format.

You can find links to all of the MassDOT IMPACT crash datasets below. Please note
that each dataset is about ~150MB and may take several minutes to download. It appears
to be slow because of the MassDOT system, or perhaps their backend which seems to point
to "opendata.arcgis.com" APIs. I also recommend not downloading multiple of them at
once because I have found that can crash your browser and even your network connection.
Not sure how, but it's happened to me a few times so you've been warned.

[2002 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2002-crashes/about)

[2003 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2003-crashes/about)

[2004 Crashes - note, the URL has a dash 1 in it for some reason...](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2004-crashes-1/about)

[2005 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2005-crashes/about)

[2006 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2006-crashes/about)

[2007 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2007-crashes/about)

[2008 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2008-crashes/about)

[2009 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2009-crashes/about)

[2010 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2010-crashes/about)

[2011 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2011-crashes/about)

[2012 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2012-crashes/about)

[2013 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2013-crashes/about)

[2014 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2014-crashes/about)

[2015 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2015-crashes/about)

[2016 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2016-crashes/about)

[2017 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2017-crashes/about)

[2018 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2018-crashes/about)

[2019 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2019-crashes/about)

[2020 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2020-crashes/about)

[2021 Crashes](https://massdot-impact-crashes-vhb.opendata.arcgis.com/datasets/MassDOT::2021-crashes/about)


To download any of these datasets, you'd just hit the "Download" button, then
hit "download" again under the CSV option. I may also post a zip archive in the 
future for the 2002 - 2016 data; based on the warning from MassDOT it would be most
accurate to download the 2017 - 2021 data live off of the MassDOT links.

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

More examples:

```python massDotParser.py csv "Medford" "Mystic Valley Parkway"```

```python massDotParser.py csv "Somerville" "Mystic Valley Parkway"```

```python massDotParser.py csv "Arlington" "Mystic Valley Parkway"```

## Tests

Currently, no formal unit tests exist for this script. I have created a list
of tests to try running before committing new code, as well as a shell script
which can be helpful to test various parameters and cases.

This is certainly something on my TODO list though, to make sure the script
is up to snuff every time I make changes to it.

Also note: tester.sh is a shell script, which can automagically generate files
for the following Cities/Roadway combinations:

| City        | Road                    |
|-------------|-------------------------|
|"Arlington"  | "Mystic Valley Parkway" |
|"Cambridge"  | "Memorial Drive"        |
|"Medford"    | "Mystic Valley Parkway" |
|"Somerville" | "Highland Ave"          |
|"Somerville" | "Mystic Valley Parkway" |

I may add more to it in the future as I become aware of roadways and Cities that
have an interest in collecting and visualing crash data

## Maps!

So far I have created two maps out of the Mass IMPACT data, which can be found below:

# City/Roadway Maps:
* [Highland Ave (Somerville, MA) Crashes](https://arcg.is/1fbfCn0)
* [Memorial Drive (Cambridge, MA) Crashes](https://arcg.is/1Tz4Pf)
* [Memorial Drive + Edwin H Land Blvd (Cambridge, MA) Crashes](https://arcg.is/1jGn8a)
* [Mystic Valley Parkway (Medford Only) Crashes](https://arcg.is/nP9mP)
* [Mystic Valley Parkway (Arlington, Medford and Somerville) Crashes](https://arcg.is/O4iin)

# Citywide Maps:
* [Boston Crashes](https://arcg.is/HKKnX)
* [Cambridge Crashes](https://arcg.is/15aO4W)
* [Medford Crashes](https://arcg.is/1nyKKz)
* [Somerville Crashes](https://arcg.is/0iKyH5)
