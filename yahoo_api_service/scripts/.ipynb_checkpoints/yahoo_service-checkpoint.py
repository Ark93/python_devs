# importing yahoo_fin lib
from yahoo_fin import stock_info
from influxdb import InfluxDBClient
from influxdb import exceptions
from datetime import datetime
import logging
import time
import pytz

logging.basicConfig(filename='service.log',level=logging.INFO)

# from influx db python documentation
json_body = [
    {
        "measurement": "mxx",
        "tags": {
            "measurement_type": "day",
            "source": "yahoo"
        },
        "time": None,
        "fields": {
            "value": None
        }
    }
]

tz = pytz.timezone('America/Mexico_City')
logging.info('Setting timezone to America/Mexico_City')

count=0
count_threshold=10
try:
    logging.info('Connecting to InfluxDB using port 8086...')
    client = InfluxDBClient('localhost', 8086)
    client.ping()
    logging.info('Connected!')
    logging.info('Reading stocks value...')
    while(True):
        value = stock_info.get_live_price('^mxx')
        json_body[0]['time'] = '{}'.format(datetime.now(tz))
        json_body[0]['fields']['value'] = value
        client.write_points(json_body, database='testdb')
        time.sleep(1)
        count=count+1
        if(count==count_threshold):
            count = 0 
            logging.info('Writing without problems')
except Exception as e:
    print('Error: {}'.format(str(e)))
    logging.error('Service stoped')
    logging.error(e)
    
