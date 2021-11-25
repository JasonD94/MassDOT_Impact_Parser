import pandas as pd
import glob
import time
import os
import sys
import logging
import argparse

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
all_data = None
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
  global all_data

  #
  # TODO: add another param for "analyzed_directory", which would be a directory
  #       to export merged/filtered CSV files
  #
  
  # Program description
  text = "This script allows you to parse MassDOT IMPACT data. You'll need to provide \
  a directory of MassDOT IMPACT data (see README for how to get this). By default, \
  this script will look in csv/ but you can provide a different directory if needed. \
  You should also pass a City and Roadway to filter on - by default, we'll parse \
  for Cambridge/Memorial Drive. In the future, you'll also be able to generate \
  data for every Town/City and Roadway in MA with a flag."
  
  # Initiate the parser
  parser = argparse.ArgumentParser(description=text)
  
  parser.add_argument("-csv", "--csv_directory", help="Which CSV directory to merge/filter from; default is csv/")
  parser.add_argument("-city", help="Which City/Town to filter the final CSV file on; default is Cambridge")
  parser.add_argument("-r", "--roadway", help="Which roadway to filter the final CSV on; default is Memorial Drive")
  parser.add_argument("-a", "--all_data", help="If set, we'll parse the MassDOT data for ALL cities & towns. This argument disregards any --city/--roadway arguments.", action='store_true')
  
  # Read arguments from the command line
  args = parser.parse_args()
  
  # You can pass in a directory to find the IMPACT CSV files from,
  # as well as a City to parse data for, and a roadway to further parse on.
  # These are optional. By default, we'll parse the following:
  # 1) Default location of "csv" inside the current working directory
  # 2) Default City of "Cambridge"
  # 3) Default roadway of "Memorial Drive"
  if args.csv_directory:
    logging.debug("found --csv_directory; setting filePath to %s" % args.csv_directory)
    filePath = args.csv_directory
  else:
    logging.warning("--csv_directory not found! Running with default csv directory")
    filePath = "csv"

  if args.city:
    logging.debug("found -city; setting City to %s" % args.city)
    city = args.city
  else:
    logging.warning("-city not found! Running with default City: 'Cambridge'")
    city = "Cambridge"

  if args.roadway:
    logging.debug("Found --roadway; setting Roadway to %s" % args.roadway)
    roadway = args.roadway
  else:
    logging.warning("--roadway not found! Running with default Roadway: 'Memorial Drive'")
    roadway = "Memorial Drive"

  if args.all_data:
    logging.info("Found --all_data param. Will disregard %s/%s and look for ALL Town/Cities and Roadways in MA instead" % (city, roadway))
    all_data = True
  else:
    logging.info("No --all_data argument provided.")
    all_data = False

  logging.info("filePath: %s" % filePath)
  logging.info("city: %s" % city)
  logging.info("roadway: %s" % roadway)
  logging.info("all_data: %s" % all_data)


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
    #       being written to the CSV files!
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
  If "--all_data" is passed, we enter this function which will:
  
  - determine all unique towns/cities in the merged_massDOT_impact_data file
  - filter the merged_massDOT_impact_data file for each town/cities specific data
  - then later filter every town/city data for all roadways in that town/city
""" 
def filterAllTowns(dframe):
  global city

  logging.info("Entered filterAllTowns()")
  
  # First, get unique City/Town names
  unique_towns = dframe["CITY_TOWN_NAME"].unique()
  unique_towns = sorted(unique_towns)
  
  logging.info("unique_towns: ")
  logging.info(unique_towns)
  
  # Next, generate all the final CSVs!
  for town in unique_towns:
    city = town
    
    logging.info("Filtering for %s town..." % city)
    
    resultDF = dframe[dframe["CITY_TOWN_NAME"].str.contains(city, case=False)]
    
    logging.info("Number of Roadways in %s: %d" % (city, resultDF["RDWY"].nunique() ) )
    logging.info("Number of crashes in %s: %d" % (city, resultDF.shape[0]))
    
    # Replace spaces and slashes with newlines
    city = town.replace("/", "_").replace(" ", "")
    
    # Check for directory's existance, create it if it doesn't
    if not os.path.exists("analyzed/towns/"):
      logging.info("analyzed/towns/ does not exist; creating it now")
      os.makedirs("analyzed/towns/")
    
    # Export the final filtered CSV to file
    resultDF.to_csv("analyzed/towns/massDOT_data_%s.csv" % city, index=False)

  
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

  # If all_data is true, we should enter filterAllTowns() to filter dframe for all
  # towns and city data we can find
  if all_data:
    dframe = pd.read_csv("analyzed/merged_massDOT_impact_data.csv", low_memory=False)
    filterAllTowns(dframe)

  else:
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
    if dframe:
      logging.info("Number of totoal rows: %d, Number of total columns: %d" % (dframe.shape[0], dframe.shape[1]))
    logging.info("Number of %s rows: %d, Number of %s columns: %d" %(city, resultDF.shape[0], city, resultDF.shape[1]))
    logging.info("Number of %s rows: %d, Number of %s columns: %d" %(roadway, finalDF.shape[0], roadway, finalDF.shape[1]))

    if dframe:
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
