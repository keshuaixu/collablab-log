from influxdb import InfluxDBClient
import requests
import logging
from credentials import influxdb_credentials, redis_credentials
import redis

logging.basicConfig(filename='error.log', format='%(asctime)s %(levelname)s %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

db = InfluxDBClient(**influxdb_credentials)
red = redis.Redis(**redis_credentials)

try:
    r = requests.get('http://collablab.wpi.edu/lab/status').json()

    try:
        red.hmset('collablab_names', r['members'])
    except Exception as e:
        logging.exception('redis fucked')

    try:
        lab_open = r['open']
        members = dict.fromkeys(r['members'], 1)
        json_body = [
            {
                'measurement': 'head_count',
                'fields': {'value': len(members)}
            }
        ]
        if len(members) > 0:
            json_body.append(
                {
                    'measurement': 'occupants',
                    'fields': members
                }
            )
        db.write_points(json_body)
    except Exception as e:
        logging.exception('influxdb fucked')

except Exception as e:
    logging.exception('collablab website fucked')
