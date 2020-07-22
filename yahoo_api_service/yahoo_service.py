# importing yahoo_fin lib
from influxdb import InfluxDBClient, exceptions
from yahoo_fin import stock_info
from datetime import datetime
import logging
import config
import time
import pytz

logging.basicConfig(filename=config.log_config.get('log_file_name'),
                    level=config.log_config.get('logging_level'),
                    format=config.log_config.get('logging_format')
                   )

# from influx db python documentation


tz = config.script_config.get('timezone')
logging.info('Setting timezone to {}'.format(tz.zone))
count=0
count_threshold=config.script_config.get('script_count_threshold')
try:
    logging.info('Connecting to InfluxDB using port {}...'.format(config.influxdb_config.get('influxdb_port')))
    client = InfluxDBClient(config.influxdb_config.get('influxdb_host'),
                            config.influxdb_config.get('influxdb_port')
                           )
    client.ping()
    client.switch_database(codockig.influxdb_config.get('influxdb_db'))
    json_body = [config.influxdb_config.get('influxdb_json_body')]
    logging.info('Connected!')
    logging.info('Reading stocks value...')
    while(True):
        if (9<=datetime.now().hour<18):
            value = stock_info.get_live_price('^mxx')
            json_body[0]['time'] = '{}'.format(datetime.now(tz))
            json_body[0]['fields']['value'] = value
            client.write_points(json_body)
            time.sleep(1)
            count=count+1
            if(count==count_threshold):
                count = 0 
                logging.info('Writing without problems')
        else:
            logging.info('BMV finished operations for today.')
            logging.info('Closing connections.')
            break
except Exception as e:
    print('Error: {}'.format(str(e)))
    logging.error('Service stoped')
    logging.error(e)
    
