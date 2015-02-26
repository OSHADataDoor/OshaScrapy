
# FYI this is still in development!

"""
The data catalog is updated approximately every other day,
so the URL  changes regularly to reflect the most current update.
We are updating the code below to add a helper function to
incorporate the latest update date into the path URL.
"""

#
#
#
#
#
#


# Title:    OSHA_ingestion.py
# Authors:  Rebecca Bilbro <bilbro@gmail.com>, Bala Venkatesan <rvbalas@gmail.com>
# Date:     Feb 26, 2015

# Special thanks to Benjamin Benfort for his support and assistance!

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
    Parses a URL and returns only the filename
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

    # Stream response and save to disk chunks at a time
    # to prevent large datasets from overwhelming the computer
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

    tasks = {
        'accident': 'osha_accident_20150223.csv.zip',
        'inspection': 'osha_inspection_20150223.csv.zip',
        'violation': 'osha_violation_20150223.csv.zip',
    }

    scrape(tasks.values())
