import os

import requests


class APIClient:
    """client for api"""

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):
        url = os.path.join(self.base_url, endpoint)
        return requests.get(url)

    def get_by_item(self, item, value):
        pass
