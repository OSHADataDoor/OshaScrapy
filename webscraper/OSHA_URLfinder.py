
"""
The CSV files with historical data on workplace inspections, violations,
and fatalities/catastrophes are updated every few days, so the URLs 
change regularly. Use BeautifulSoup to find the latest URLs to use in
the OSHA_ingestion.py file provided at 
http://github.com/OSHADataDoor/OshaScrapy/tree/master/webscraper
"""

##########################################################################
## Imports
##########################################################################
import mechanize
from bs4 import BeautifulSoup


##########################################################################
## Make Soup
##########################################################################
CATALOGS_URL  = "http://ogesdw.dol.gov/views/data_catalogs.php"

br = mechanize.Browser()
br.set_handle_robots(False)
br.open(CATALOGS_URL)

form = br.select_form(name="osha_metadata")
res = br.submit()
content = res.read()

soup = BeautifulSoup(content)

##########################################################################
## Accidents
## CSV will look something like "osha_accident_20######.csv.zip" 
##########################################################################
"""
ACCIDENTS: These are all fatalities and catastrophes reported by
employers to OSHA since the 1970's. Catastrophes are defined as 
the work-related hospitalization of 3 or more workers. The 
database captures these consistently and reliably starting 1990, 
and a 2011 system upgrade makes most reliable time series slice 
roughly 1990-2010.
"""
accidents = soup.select('a[href*="/osha_accident_20"]')
print "Accidents filename: ", "\n", accidents

##########################################################################
## Inspections
## CSV will look something like "osha_inspection_20######.csv.zip" 
##########################################################################
"""
INSPECTIONS: These are all closed inspections conducted by Federal
OSHA and State Plan states (non-Federal jusidictions) since the 
1980's. The database captures these consistently and reliably 
starting 1990, and a 2011 system upgrade makes most reliable time 
series slice roughly 1990-2010. 
"""
inspections = soup.select('a[href*="/osha_inspection_20"]')
print "Inspections filename: ", "\n", inspections
##########################################################################
## Violations
## CSV will look something like "osha_violation_20######.csv.zip" 
##########################################################################
"""
VIOLATIONS: These are all violations found by either Federal OSHA
or State Plan states (non-Federal jusidictions) since the 
1980's. The database captures these consistently and reliably 
starting 1990, and a 2011 system upgrade makes most reliable time 
series slice roughly 1990-2010.
"""
violations = soup.select('a[href*="/osha_violation_20"]')
print "Violations filename: ", "\n", violations
