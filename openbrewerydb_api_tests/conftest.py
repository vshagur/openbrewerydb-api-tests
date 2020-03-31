import pytest

from openbrewerydb_api_tests import client
from openbrewerydb_api_tests import constants
from openbrewerydb_api_tests import validator


def pytest_addoption(parser):
    parser.addoption(
        '--url',
        action='store',
        default=constants.DEFAULT_URL,
        help=f'Base URL for API, by default - {constants.DEFAULT_URL}.'
    )

    parser.addoption(
        '--delay',
        action='store',
        type=int,
        default=constants.DEFAULT_REQUEST_DELAY,
        help=f'Delay between API requests, by default - {constants.DEFAULT_REQUEST_DELAY}.'
    )


@pytest.fixture(scope="session")
def api_client(request):
    base_url = request.config.getoption("--url")
    delay = request.config.getoption("--delay")
    templates = constants.EndpointTemplates
    return client.APIClient(base_url=base_url, delay=delay, templates=templates)


@pytest.fixture(scope='session')
def field_validator():
    return validator.BrewerySchema()
