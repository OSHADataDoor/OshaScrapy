"""
NOTE:

The CSV files with historical data on workplace inspections, violations,
and fatalities/catastrophes are updated every few days, so the URLs
change regularly. 

Before running this program, use OSHA_URLfinder.py provided at:
http://github.com/OSHADataDoor/OshaScrapy/tree/master/webscraper
to identify the latest URL names and update the task list below.

"""

# Title:    OSHA_ingestion.py
# Authors:  Rebecca Bilbro <bilbro@gmail.com>, Bala Venkatesan <rvbalas@gmail.com>
# Date:     March 1, 2015

# Special thanks to Benjamin Bengfort for his support and assistance!

"""
Ingest data on workplace fatalities, investigations, and violations
from the OSHA data catalog. 
"""

##########################################################################
## Imports
##########################################################################
import os
import re
import sys
import requests
import mechanize

from urlparse import urlsplit, urljoin

##########################################################################
## Fixtures
##########################################################################
DATA_URL_BASE = "http://prd-enforce-xfr-02.dol.gov/data_catalog/OSHA/"
CATALOGS_URL  = "http://ogesdw.dol.gov/views/data_catalogs.php"

##########################################################################
## Helper functions
##########################################################################

def filename_from_url(url):
    """
    Parses a URL and returns the filename
    """
    parts = urlsplit(url)
    return os.path.basename(parts.path)

def download_osha_data(url, path=None):
    """
    Downloads a file and writes it to disk at the path or breaks apart
    the URL to get a file name to save it to the current working dir.
    """

    # If path is None, save to the URL basename
    path = path or filename_from_url(url)

    # Stream response and save to disk in chunks
    response = requests.get(url, stream=True)
    with open(path, 'w') as out:
        for chunk in response.iter_content(chunk_size=16384):
            out.write(chunk)

def scrape(paths, base=DATA_URL_BASE):
    """
    Download all data given an iterable of paths
    """

    for path in paths:
        url = urljoin(base, path)
        download_osha_data(url)

if __name__ == '__main__':

    # Remember to update the task assignments below using the
    # latest URL names! These were the paths as of 3/4/2015
    tasks = {
        'accident': 'osha_accident_20150302.csv.zip',
        'inspection': 'osha_inspection_20150304.csv.zip',
        'violation': 'osha_violation_20150304.csv.zip',
    }

    scrape(tasks.values())
