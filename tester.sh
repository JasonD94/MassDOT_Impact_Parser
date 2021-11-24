#!/bin/bash

# This script runs a bunch of test cases against the massDotParser.py script
# It can also be used to generate files of interest, which is especially helpful
# when generating new files after adding new data

python massDotParser.py csv "Arlington" "Mystic Valley Parkway"
python massDotParser.py csv "Boston" "Memorial Drive"
python massDotParser.py csv "Cambridge" "Memorial Drive"
python massDotParser.py csv "Cambridge" "Edwin Land Blvd"
python massDotParser.py csv "Cambridge" "Edwin"
python massDotParser.py csv "Medford" "Mystic Valley Parkway"
python massDotParser.py csv "Somerville" "Highland Ave"
python massDotParser.py csv "Somerville" "Mystic Valley Parkway"
