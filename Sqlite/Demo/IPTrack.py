#!/usr/bin/env python

import sqlite3
import urllib2
from datetime import datetime

dbfile = 'database.db'

connection = sqlite3.connect(dbfile)
cursor = connection.cursor()

# Current date/time
d = datetime.now()

# Get the current IP
req = urllib2.Request('https://api.ipify.org')
res = urllib2.urlopen(req)
ip = res.read()

# Input the IP into the log
cursor.execute("INSERT INTO IP_LOG (date, ip) VALUES (?, ?)", (d, ip, ))
ipresult = cursor.execute("SELECT ip from IP_CURRENT").fetchone()
oldip = ""
if ipresult != None:
	oldip = ipresult[0]
if ip != oldip:
	cursor.execute("UPDATE IP_CURRENT SET ip=?", (ip, ))
	cursor.execute("INSERT INTO IP_CHANGES (date, ip) VALUES (?, ?)", (d, ip, ))
	# Send alert

connection.commit()
