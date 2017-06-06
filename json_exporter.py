# coding=utf-8

import sys
import json
import time
try:
    import urllib2
except:
    # Python 3
    import urllib.request as urllib2

from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY


class JSONCollector(object):
    def __init__(self, faked=True):
        self.faked = faked

    @property
    def faked_json(self):
        return {
            "requests_duration_seconds": 1.2
        }

    def fetch_json(self):
        if not self.faked:
            raise Exception("Not implement for reading JSON file data.")
        else:
            return self.faked_json

    def collect(self):
        # The metrics we want to export.
        # same with CounterMetricFamily, SummaryMetricFamily
        # details refer to: https://github.com/prometheus/client_python
        metric = GaugeMetricFamily(
            'requests_duration_seconds',
            'requests duration seconds for demo',  # HELP MSG
            labels=["some_labels_here_for_metric", "add_metric_could_define"]
        )

        json_data = self.fetch_json()
        metric.add_metric(["faked_request_host_label",
                           "faked_request_list_labels"],
                          json_data["requests_duration_seconds"])
        yield metric

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        sys.stderr.write("Usage: json_exporter.py <JSON_FILE_PATH_OR_USE_DEFAULT_FAKED_JSON>\n")
        sys.exit(1)
    elif len(sys.argv) == 2:
        faked = False
    else:
        faked = True

    REGISTRY.register(JSONCollector(faked))
    start_http_server(9118)
    print("json_exporter start at 0.0.0.0:9118...")

    while True:
        time.sleep(1)
