from influxdb import InfluxDBClient
import requests
import logging
from credentials import influxdb_credentials

logging.basicConfig(filename='error.log', format='%(asctime)s %(levelname)s %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

db = InfluxDBClient(**influxdb_credentials)

try:
    r = requests.get('http://collablab.wpi.edu/lab/status').json()
    lab_open = r['open']
    members = dict.fromkeys(r['members'], 1)
    if len(members) > 0:
        json_body = [
            {
                'measurement': 'occupants',
                'fields': members
            }
        ]
        db.write_points(json_body)

except Exception as e:
    logging.exception('bork')
