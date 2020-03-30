import os

import pytest
import requests

DEFAULT_URL = 'https://api.openbrewerydb.org/'
DEFAULT_REQUEST_DELAY = 1


class APIClient:
    """client for api"""
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):
        url = os.path.join(self.base_url, endpoint)
        return requests.get(url)

    def get_by_item(self, item, value):
        pass


def pytest_addoption(parser):
    parser.addoption(
        '--url',
        action='store',
        default=DEFAULT_URL,
        help=f'Base URL for API, by default - {DEFAULT_URL}.'
    )

    parser.addoption(
        '--delay',
        action='store',
        type=int,
        default=DEFAULT_REQUEST_DELAY,
        help=f'Delay between API requests, by default - {DEFAULT_REQUEST_DELAY}.'
    )


@pytest.fixture(scope="session")
def api_client(request):
    base_url = request.config.getoption("--url")
    return APIClient(base_url=base_url)
