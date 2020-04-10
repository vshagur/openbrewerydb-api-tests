import os
import time

import requests


class APIClient:
    """client for api"""

    def __init__(self, base_url, delay, templates):
        self.base_url = base_url
        self.delay = delay
        self.templates = templates

    def get(self, endpoint):
        url = os.path.join(self.base_url, endpoint)
        time.sleep(self.delay)
        return requests.get(url)

    def get_filter_by(self, field_name, value):
        endpoint = self.templates[field_name].format(value)
        return self.get(endpoint)
