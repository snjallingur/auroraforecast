# Aurora Forecast for Iceland
Home Assistant MQTT sensor(s) for aurora forecast in Iceland
based on:
[http://gagnaveita.vegagerdin.is/api/faerd2017_1](https://xmlweather.vedur.is/aurora?op=xml&type=index)

more information about the returned response can be found here:
http://www.vegagerdin.is/vefur2.nsf/Files/gagnaveita_faerd_2017/$file/gagnaveita_faerd_2017.pdf

The sensors are created from a python script ("auroraforecast.py"). The script extracts the information from the xml file and pushes the information to a MQTT topic. The Aurora forecast is provided for the next 10 days. You can define in your mqtt.conf file how many. sensor you want to include. Usually the information for actual day ("today_0") and the following day ("today_1") should usually be enough.

You can then leverage that information to send you a notification when it is very likely that you can experience an aurora experience in a sunny condition and when the sun is below the horizon. An example can be found in "automation.yaml".

The Python script can be run as a shell command or a cron job.

# Example Lovelace card
The code for the gauge can be found in lovelace.yaml
![GitHub Logo](/lovelace_auroraforecast.jpg)
