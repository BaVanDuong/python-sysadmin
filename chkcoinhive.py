#!/usr/bin/python
# Check website have script coin-hive
# Add urls list in one file then run script
# Example: chkcoinhive urls.txt
# please using python 3 installed module bs4, lxml

import requests
import sys
from bs4 import BeautifulSoup

OK = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

src = sys.argv[1]
with open(src) as urls:
    for url in urls:
        try:
            url = url.rstrip('\n')
            r = requests.get(url)
            soup = BeautifulSoup(r.content,"lxml")
            flag=False
            for i in soup.find_all("script"):
                if (i.get("src") and 'coinhive' in i.get("src")):
                    flag=True
                    print(FAIL+"Found script coin-hive {0} on {1}".format(i.get('src'),url)+ENDC)
            if(not flag):
                print(OK+"Not found coin-hive on site "+ url+ENDC)
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)

