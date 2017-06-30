#!/usr/bin/python

import json
import sys
import time
import datetime

import Adafruit_DHT
import gspread
from oauth2client.service_account import ServiceAccountCredentials


DHT_TYPE = Adafruit_DHT.DHT11


DHT_PIN  = 21


GDOCS_OAUTH_JSON       = 'Temperature Sensor Readings-f35067ee18d3.json'


GDOCS_SPREADSHEET_NAME = 'Temperature Sensor Readings'

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 5


def login_open_sheet(oauth_key_file, spreadsheet):
    """Connect to Google Docs spreadsheet and return the first worksheet."""
    try:
        scope =  ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
        gc = gspread.authorize(credentials)
        worksheet = gc.open(spreadsheet).sheet1
        return worksheet
    except Exception as ex:
        print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)


print('Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS))
print('Press Ctrl-C to quit.')
worksheet = None
while True:
    print('loop running')
    if worksheet is None:
        worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)

    # Attempt to get sensor reading.
    humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)

    if humidity is None or temp is None:
	print('hello')
        time.sleep(2)
        continue

    print('Temperature: {0:0.1f} C'.format(temp))
    print('Humidity:    {0:0.1f} %'.format(humidity))


    try:
        worksheet.append_row((datetime.datetime.now(), temp, humidity))
    except:

        print('Append error, logging in again')
        worksheet = None
        time.sleep(FREQUENCY_SECONDS)
        continue


    print('Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME))
time.sleep(FREQUENCY_SECONDS)
