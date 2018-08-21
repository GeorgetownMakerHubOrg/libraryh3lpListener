#!/usr/bin/env python

# current-activity.py
# -------------------
# Count the number of active chats and the number of librarians that
# are staffing services.

# install:
# sudo pip install adafruit-io
# git clone https://github.com/GeorgetownMakerHubOrg/libraryh3lpListener.git
## get the libraryh3lp-sdk-python in the same folder as this file.

from datetime import datetime
# Import standard python modules
import time

# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed

import lh3.api
import secrets

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = secrets.AIO_KEY

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'gumakerhub'
ADAFRUIT_IO_FEEDNAME = 'makerhubevents.signagemessage'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client = lh3.api.Client()




while True:
    # Fetch today's chats.
    now  = datetime.now()
    chats = client.chats().list_day(now.year, now.month, now.day)

    num_active = 0
    num_unanswered = 0
    for chat in chats:
        print(chat)
        if chat['ended']:
            continue
        if chat['queue'] != 'gt-makerhub':
            continue

        # Only count those starting in the last 15 minutes.
        started = datetime.strptime(chat['started'], '%Y-%m-%d %H:%M:%S')
        if (now - started).total_seconds() >= 900:
            continue

        if chat['accepted']:
            num_active += 1
        else:
            num_unanswered += 1
            print("this unanswered chat")
            print(chat['queue'])

    print('{} active chats, {} unanswered'.format(num_active, num_unanswered))

    if num_unanswered > 0:
        print ("SEND AN ALERT NOW!!!")
        aio.send_data(ADAFRUIT_IO_FEEDNAME, "Incoming Chat!")

    time.sleep(10)



