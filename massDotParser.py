import pandas as pd
import glob

"""
    This script will:
    
    * Merge several MassDOT CSV files that have been exported from
      the MassDOT Crash Open Data Portal aka IMPACT
    * CSV files can be exported from the following site:
      https://massdot-impact-crashes-vhb.opendata.arcgis.com/
    * Search for years, such as "2010 Crashes"
"""

filePath = None
city = None
roadway = None

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
  print("Command argv[1] not found! Running with default csv directory")
  filePath = "csv/"

try:
  city = sys.argv[2]
except:
  print("Command argv[2] not found! Running with default City: Cambridge")
  city = "CAMBRIDGE"
    
try:
  roadway = sys.argv[3]
except:
  print("Command argv[3] not found! Running with default Roadway: Memorial Drive\n")
  roadway = "Memorial Drive"


print("filePath: %s" % filePath)
print("city: %s" % city)
print("roadway: %s" % roadway)

# Stealing this code of Stackoverflow:
# https://stackoverflow.com/a/21232849
all_files = glob.glob(filePath + "/*.csv")

li = []

for filename in all_files:
	df = pd.read_csv(filename, index_col=None, header=0)
	li.append(df)

dframe = pd.concat(li, axis=0, ignore_index=True)

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
resultDF.to_csv("analyzed/filtered_massDOT_data_%s.csv" % city, index=True)

# Do some stats too

