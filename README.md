# influxdb-ticket-tracker
InfluxDB + Stubhub ( Taylor's Version )

Fetches ticket data for a list of Eras Tour dates writes them to an InfluxDB bucket


## Setup

`pip install -r requirements.txt`

```bash
export INFLUX_URL="http://localhost:8086"
export INFLUX_TOKEN="your-token"
export INFLUX_ORG="org-name"
export INFLUX_BUCKET="bucket-name"
```

`python main.py`


## Grafana Screenshot

By configuring Grafana with an InfluxDB Data Source, you can plot the mean price, track new listings, "quality score, and "deal score" from Stubhub

![look at this graph](https://github.com/topherbullock/influxdb-ticket-tracker/assets/1895900/f54e6428-e4af-4a76-b081-17027e18f253)
