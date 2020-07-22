import logging
import pytz

log_config={
    'log_file_name' : 'yahoo_service.log',
    'logging_level' : logging.INFO,
    'logging_format' : '%(asctime)s %(message)s' ,
}

influxdb_config={
    
    'influxdb_host' : '172.18.0.2', #check the ipv4 from docker network
    'influxdb_port' : 8086,
    'influxdb_db' : 'testdb',
    'influxdb_json_body' : {
        "measurement": "mxx",
        "tags": {
            "measurement_type": "day",
            "source": "yahoo"
        },
        "time": None,
        "fields": {
            "value": None
        }
    },
}

script_config={    
    'timezone' : pytz.timezone('America/Mexico_City'),
    'script_count_threshold':10
}
