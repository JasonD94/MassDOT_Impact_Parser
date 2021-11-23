import pandas as pd
import glob
import time
import os
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

"""
	merges all CSV files found under filePath. They should look like this:
	2010_Crashes.csv
	2011_Crashes.csv
	...
	2020_Crashes.csv
	2021_Crashes.csv
"""
def mergeCsvFiles():
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
	
	return dframe
	
"""
	main driver of the script
"""
def main():

	global filePath
	global city
	global roadway

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
		filePath = "csv"

	try:
		city = sys.argv[2]
	except:
		logging.warning("Command argv[2] not found! Running with default City: 'Cambridge'")
		city = "cambridge"

	"""
		NOTE: there's a freaking space in the RDWAY column data...
					TODO: figure out how to do a "grep" like match for a roadway
								but for now I'm just adding in a space at the beginning...
	"""
	try:
		roadway = sys.argv[3]
	except:
		logging.warning("Command argv[3] not found! Running with default Roadway: 'Memorial Drive'")
		roadway = "Memorial Drive"

	logging.info("filePath: %s" % filePath)
	logging.info("city: %s" % city)
	logging.info("roadway: %s" % roadway)

	# Skip processing the CSV files if the 'merged_massDOT_impact_data.csv' already exists
	dframe = None
	
	# TODO: make this param and check that the directory exists
	filePathCheck = "analyzed/merged_massDOT_impact_data.csv"
	
	if not os.path.exists(filePathCheck):
		logging.debug("merged_massDOT_impact_data.csv does NOT exist, generating it now!")
		dframe = mergeCsvFiles()
	else:
		logging.debug("merged_massDOT_impact_data.csv exists!")
		dframe = pd.read_csv("analyzed/merged_massDOT_impact_data.csv", low_memory=False)

	logging.info("dframe columns: %s" % dframe.columns)
	logging.info("dframe columns: %s" % dframe.columns.tolist())

	# dframe should have all the data we want now. Let's filter it by "CITY_TOWN_NAME"
	# and "RDWY"
	# Also, let's export dframe to a file too.
	#
	# NOTE: make this an optional param. It took like 2GB of RAM and a solid minute
	# or two to run on my machine.
	#dframe.to_csv("analyzed/merged_massDOT_impact_data.csv")

	# Switching to using .contains() instead of == so we can find matches that aren't
	# 100% matches. Some columns have stuff like:
	# "HIGHLAND AVENUE / TOWER STREET" that we won't match on if we're too strict
	# about it. Also using case=False to avoid doing .upper() calls
	resultDF = dframe[dframe["CITY_TOWN_NAME"].str.contains(city, case=False)]

	# Export the final filtered CSV to file
	# index=True required to get the first column to show up; see this SO post:
	# https://stackoverflow.com/a/62299935
	resultDF.reset_index()
	resultDF.to_csv("analyzed/massDOT_data_%s.csv" % city)

	# Filter down to RDWY too
	finalDF = resultDF[resultDF["RDWY"].str.contains(roadway, case=False, na=False)]
	finalDF.to_csv("analyzed/massDOT_data_%s%s.csv" % (city, roadway.replace(" ", "_")))

	# Do some stats too
	logging.info("*************************************************************************************************")
	logging.info("Number of totoal rows: %d, Number of total columns: %d" % (dframe.shape[0], dframe.shape[1]))
	logging.info("Number of %s rows: %d, Number of %s columns: %d" %(city, resultDF.shape[0], city, resultDF.shape[1]))
	logging.info("Number of %s rows: %d, Number of %s columns: %d" %(roadway, finalDF.shape[0], roadway, finalDF.shape[1]))

	logging.info("Number of Roadways in Combined CSV: %d" % ( dframe["RDWY"].nunique() ) )
	logging.info("Number of Roadways in Cambridge: %d" % ( resultDF["RDWY"].nunique() ) )
	logging.info("Number of crashes in %s on %s: %d" % (city, roadway, finalDF.shape[0]))

	# Debug - how long the script takes to run
	executionTime = (time.time() - startTime)
	logging.info('Execution time in seconds: %.2f seconds' % round(executionTime, 2))

main()
