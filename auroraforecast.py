import logging
# initialize the log settings
logging.basicConfig(filename = '/home/homeassistant/.homeassistant/snjallingur_scripts/pythonscripts.log', level = logging.DEBUG)
logging.info('logger for nordurljósaspa started')
import sys

try: 
    import requests
    from bs4 import BeautifulSoup
    import time
    from datetime import datetime
    import xml.etree.ElementTree as ET
    import paho.mqtt.client as paho
    import json
    import datetime
    from datetime import date
except (ImportError,ModuleNotFoundError) as i:
    logging.exception('Import error: ' + str(i))  

todaydateobject = datetime.date.today()

#MQTT Broker settings
#Adjust to your environment
broker="localhost"
# create client and connect to broker
client= paho.Client("nordurljos")
client.username_pw_set(username="homeassistant",password="snjallingur")
client.connect(broker)
client.publish("homeassistant/nordurljosaspa","running")
# Frekari upplýsingar um skiluð svör:
# https://www.vedur.is/skjol/vefur/XML-thjonusta-090813.pdf
#
url = 'https://xmlweather.vedur.is/aurora?op=xml&type=index'

#response = requests.get(url).json()
#print(response)
try:
    document = requests.get(url, verify=False)
    nordurljosaspa = BeautifulSoup(document.content,"lxml-xml")
    content = nordurljosaspa.find_all("night_data")       
except (IOError,NameError) as e:
    logging.exception(str(e)) 
    logging.error('Error occurred ' + str(e)) 

today_0 = {}
today_1 = {}
#print(content)
#print(content[0]['aurora']['night_data'][0])
for evening_date in content:
    #print(evening_date['night_data'])
    datestring = evening_date.find("evening_date").string
    nordurdurljosactivity = evening_date.find("activity_forecast").string
    #print(datestring)
    dateobject = datetime.datetime.strptime(datestring, "%Y-%m-%d").date()
    #print(str(dateobject.year) + "." + str(dateobject.month))
    daysdelta = dateobject - todaydateobject
    #print(daysdelta.days)
    sensor_name = "today_" + str(daysdelta.days)
    #print(sensor_name)
    #print(nordurdurljosactivity)
    #forecasts = station.find_all("activity_forecast")
    try:
        client.publish("homeassistant/nordurljosaspa/" + sensor_name,nordurdurljosactivity)
    except:
        logging.error('Couldn´t publish to MQTT broker: ' + str(broker))
