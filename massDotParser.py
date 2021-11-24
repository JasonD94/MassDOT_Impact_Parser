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
    * Filter based on a provided City / Roadway name
		
		The README has more details on where to get the MassDOT CSV files for
		the merging & filtering, as well as examples of running this script.
"""

# Variables
filePath = None
city = None
roadway = None
startTime = time.time()

# Logging setup
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='massDotParser.log')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.info("Starting massDotParser.py")

# Additional logging setup - show ALL column names
# https://stackoverflow.com/a/49189503
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# The fields we care about
fields = ["CITY_TOWN_NAME", "RDWY"]


"""
	Handles command line argument processing
"""
def handleCmdArgs():
	global filePath
	global city
	global roadway

	# TODO: make these args like 'path=xyz', so that we can call the script
	#       with these arguments in different orders, or ignore/default some
	#       arguments. right now you HAVE to give a path, even if you're ok
	#       with the default csv directory.
  #
	# TODO: add another param for "analyzed_directory", which would be a directory
	#       to export merged/filtered CSV files
	#
	
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

		# NOTE: index=False is required in to_csv to avoid the index column from 
		#			  being written to the CSV files!
		#       See: https://stackoverflow.com/a/57179677 for more details

		'''
			NOTE: low_memory=False is hacky. TODO: fix the DtypWarning: Columns have mixed types.
				https://stackoverflow.com/a/27232309
			Errors look like:
				sys:1: DtypeWarning: Columns (34) have mixed types. Specify dtype option on import or set low_memory=False.
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
	
	# Export to disk to speed up future runs
	# Ignore the first column with index=False
	# https://stackoverflow.com/a/25230582
	dframe.to_csv("analyzed/merged_massDOT_impact_data.csv", index=False)
	
	return dframe
	
"""
	Filters the CSV file by City / Roadway
	First checks to see if we've already filtered this City before, to avoid
	reading in the ~2GB merged CSV file.
	It also checks to see if we've already filtered this roadway before, and
	will skip processing if so while logging a warning for us to know what happened.
"""
def filterCsvFiles():
	# Skip processing the CSV files if the 'merged_massDOT_impact_data.csv' already exists
	dframe = None
	
	# TODO: make this param and check that the directory exists
	filePathCheck = "analyzed/merged_massDOT_impact_data.csv"
	cityPathCheck = "analyzed/massDOT_data_%s.csv" % city
	roadwayPathCheck = "analyzed/massDOT_data_%s_%s.csv" % (city, roadway.replace(" ", "_"))
	
	if not os.path.exists(filePathCheck):
		logging.debug("merged_massDOT_impact_data.csv does NOT exist, generating it now!")
		dframe = mergeCsvFiles()
	else:
		logging.debug("merged_massDOT_impact_data.csv exists!")
		
		# To speed up future runs, if the City file already exists, let's filter
		# off of that instead of loading in a ~2GB file and filtering it again.
		if not os.path.exists(cityPathCheck):
			dframe = pd.read_csv("analyzed/merged_massDOT_impact_data.csv", low_memory=False)

	# Skip this logic if we already determined the City filtered file exists
	if not os.path.exists(cityPathCheck):
		# Switching to using .contains() instead of == so we can find matches that aren't
		# 100% matches. Some columns have stuff like:
		# "HIGHLAND AVENUE / TOWER STREET" that we won't match on if we're too strict
		# about it. Also using case=False to avoid doing .upper() calls
		resultDF = dframe[dframe["CITY_TOWN_NAME"].str.contains(city, case=False)]
		
		# Export the final filtered CSV to file
		resultDF.to_csv("analyzed/massDOT_data_%s.csv" % city, index=False)
	else:
		resultDF = pd.read_csv(cityPathCheck, low_memory=False)

	# Filter down to RDWY too, assuming we didn't already do this
	if os.path.exists(roadwayPathCheck):
		logging.warning("Parsed file already exists: %s" % roadwayPathCheck)
		exit()
	
	finalDF = resultDF[resultDF["RDWY"].str.contains(roadway, case=False, na=False)]
	finalDF.to_csv("analyzed/massDOT_data_%s_%s.csv" % (city, roadway.replace(" ", "_")), index=False)

	# Do some stats too
	#(make sure to ignore the merged stats if we're skipping them!)
	logging.info("*****************************************************************************")
	if not os.path.exists(filePathCheck):
		logging.info("Number of totoal rows: %d, Number of total columns: %d" % (dframe.shape[0], dframe.shape[1]))
	logging.info("Number of %s rows: %d, Number of %s columns: %d" %(city, resultDF.shape[0], city, resultDF.shape[1]))
	logging.info("Number of %s rows: %d, Number of %s columns: %d" %(roadway, finalDF.shape[0], roadway, finalDF.shape[1]))

	if not os.path.exists(filePathCheck):
		logging.info("Number of Roadways in Combined CSV: %d" % ( dframe["RDWY"].nunique() ) )
	logging.info("Number of Roadways in %s: %d" % (city, resultDF["RDWY"].nunique() ) )
	logging.info("Number of crashes in %s on %s: %d" % (city, roadway, finalDF.shape[0]))

"""
	main driver of the script
"""
def main():

	handleCmdArgs()
	filterCsvFiles()

main()

# Debug - how long the script takes to run
executionTime = (time.time() - startTime)
logging.info('Execution time in seconds: %.2f seconds' % round(executionTime, 2))
