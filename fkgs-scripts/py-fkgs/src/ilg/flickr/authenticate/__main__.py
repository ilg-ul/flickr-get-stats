"""
Usage:
    python -m ilg.flickr.statistics.get.csv [options]

Options:
    -f "FOLDER", --folder="FOLDER"
        destination folder where CSV files are stored; 
        default is '$HOME/Documents/Flickr/Statistics'

    -d "DAY", --day="DAY"
        the day to get statistics for; the format is 
        quite strict, and should look like "2010-06-30"
     
    -v, --verbose
        print progress output

    -V, --version
        print program version

    -h, --help
        print this message

Purpose:
    Retrieve daily CSV statistic files for a Flickr account.

---

This program will generate one CSV file per day. The file format is 
exactly the same as used by Flickr in the past, when they provided 
aggregated statistics.

The output files contain the date in the file name, like:
    2010-06-30-flickr.csv
    
The files already present in the destination folder are not 
fetched again.

The program will try to go back in time and fetch as much 
statistics as possible, about one month (according to Flickr, 
at least 28 days are stored). 

If the --day option is used, only one day of statistics is fetched.

The authentication is done only once, and the Flickr authentication 
token is stored in the user home directory.
 
"""

import flickrapi
import webbrowser
import sys
import time
import getopt
import os
import requests
#import ssl

from ilg.flickr.statistics.get.aggregate import Aggregate
from ilg.flickr.statistics.get.csv.writer import Writer


'''
The below key identifies this application only, for accessing Flickr.
It is not suitable for other purposes.
'''
api_key = '972a07f9991a94960fee5bde355b7191'
api_secret = '4573a0d92f02730b'

# ---------------------------------------------------------------------
def usage():
    print __doc__

def main(*argv):
       
    # authenticate
    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    flickr.authenticate_via_browser(perms='read')
 
    for retry in range(10):
        try:
            eRsp = flickr.urls_getUserPhotos()
            break
        except Exception as ex:
            print '>>>>>>>>>> urls_getUserPhotos %s' % ex   

    eUser = eRsp.find('user')
    sUrl = eUser.attrib.get('url')
    print sUrl
    print '[done]'
    return 0

if __name__ == '__main__':
    sys.exit(main(*sys.argv))

