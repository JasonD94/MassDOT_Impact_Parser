import pandas as pd
import glob
import time
import sys
import logging

"""
    This script will:
    
    * Merge several MassDOT CSV files that have been exported from
      the MassDOT Crash Open Data Portal aka IMPACT
    * CSV files can be exported from the following site:
      https://massdot-impact-crashes-vhb.opendata.arcgis.com/
    * Search for years, such as "2010 Crashes"
"""

# Variables
filePath = None
city = None
roadway = None
startTime = time.time()

# Logging setup
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG, filename='massDotParser.log')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.info("Starting massDotParser.py")

# Additional logging setup - show ALL column names
# https://stackoverflow.com/a/49189503
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# The fields we care about
fields = ["CITY_TOWN_NAME", "RDWY"]


# You can pass in a directory to find the IMPACT CSV files from,
# as well as a City to parse data for, and a roadway to further parse on.
# These are optional. By default, we'll parse the following:
# 1) Default location of "csv" inside the current working directory
# 2) Default City of "Cambridge"
# 3) Default roadway of "Memorial Drive"
try:
  filePath = sys.argv[1]
except:
  logging.warning("Command argv[1] not found! Running with default csv directory")
  filePath = "csv/"

try:
  city = sys.argv[2].upper()
except:
  logging.warning("Command argv[2] not found! Running with default City: Cambridge")
  city = "cambridge".upper()
    
try:
  roadway = sys.argv[3]
except:
  logging.warning("Command argv[3] not found! Running with default Roadway: Memorial Drive")
  roadway = "Memorial Drive"

logging.debug("filePath: %s" % filePath)
logging.debug("city: %s" % city)
logging.debug("roadway: %s" % roadway)

# Stealing this code of Stackoverflow:
# https://stackoverflow.com/a/21232849
all_files = glob.glob(filePath + "/*.csv")

li = []

for filename in all_files:

	# NOTE: low_memory=False is hacky. TODO: fix the DtypWarning: Columns have mixed types.
	# https://stackoverflow.com/a/27232309
	'''
	Errors look like:
		sys:1: DtypeWarning: Columns (34) have mixed types. Specify dtype option on import or set low_memory=False.
		sys:1: DtypeWarning: Columns (33) have mixed types. Specify dtype option on import or set low_memory=False.
		sys:1: DtypeWarning: Columns (30,33,58) have mixed types. Specify dtype option on import or set low_memory=False.
		sys:1: DtypeWarning: Columns (34,109) have mixed types. Specify dtype option on import or set low_memory=False.
		sys:1: DtypeWarning: Columns (29,33,34,109) have mixed types. Specify dtype option on import or set low_memory=False.
		sys:1: DtypeWarning: Columns (29,30,67) have mixed types. Specify dtype option on import or set low_memory=False.
		sys:1: DtypeWarning: Columns (66) have mixed types. Specify dtype option on import or set low_memory=False.
		sys:1: DtypeWarning: Columns (95,107) have mixed types. Specify dtype option on import or set low_memory=False.
		sys:1: DtypeWarning: Columns (28) have mixed types. Specify dtype option on import or set low_memory=False.
	'''
	df = pd.read_csv(filename, low_memory=False)
	
	logging.debug("df columns: %s" % df.columns)
	logging.debug("df columns: %s" % df.columns.tolist())
	
	li.append(df)

'''
TODO: investigate the FutureWarning about sorting:
massDotParser.py:81: FutureWarning: Sorting because non-concatenation axis is not aligned. A future version
of pandas will change to not sort by default.

For now, setting sort=False
'''
dframe = pd.concat(li, axis=0, sort=False)

logging.debug("dframe columns: %s" % dframe.columns)
logging.debug("dframe columns: %s" % dframe.columns.tolist())

# dframe should have all the data we want now. Let's filter it by "CITY_TOWN_NAME"
# and "RDWY"
# Also, let's export dframe to a file too.
#
# NOTE: make this an optional param. It took like 2GB of RAM and a solid minute
# or two to run on my machine.
#dframe.to_csv("analyzed/merged_massDOT_impact_data.csv")

resultDF = dframe[dframe["CITY_TOWN_NAME"] == city]
#resultDF = resultDF[resultDF["RDWY"] == roadway]

# Export the final filtered CSV to file
# index=True required to get the first column to show up; see this SO post:
# https://stackoverflow.com/a/62299935
resultDF.reset_index()
resultDF.to_csv("analyzed/filtered_massDOT_data_%s.csv" % city)

# Do some stats too


# Debug - how long the script takes to run
executionTime = (time.time() - startTime)
logging.info('Execution time in seconds: %.2f seconds' % round(executionTime, 2))
