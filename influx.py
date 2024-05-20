import influxdb_client, os
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.getenv("INFLUX_TOKEN")
org = os.getenv("INFLUX_ORG")
url = os.getenv("INFLUX_URL")
bucket= os.getenv("INFLUX_BUCKET")

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

def write(record):
    write_api.write(bucket=bucket, record=record)

