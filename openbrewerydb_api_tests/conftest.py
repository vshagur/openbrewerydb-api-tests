import pytest

from openbrewerydb_api_tests import client
from openbrewerydb_api_tests import constants as CONST
from openbrewerydb_api_tests import dump_db
from openbrewerydb_api_tests import validator


def pytest_addoption(parser):
    """adds command line options"""

    parser.addoption(
        '--url',
        action='store',
        default=CONST.DEFAULT_URL,
        help=f'Base URL for API, by default - {CONST.DEFAULT_URL}.'
    )

    parser.addoption(
        '--delay',
        action='store',
        type=int,
        default=CONST.DEFAULT_REQUEST_DELAY,
        help=f'Delay between API requests, by default - {CONST.DEFAULT_REQUEST_DELAY}.'
    )


@pytest.fixture(scope="session")
def api_client(request):
    """provides a client for working with api"""

    base_url = request.config.getoption("--url")
    delay = request.config.getoption("--delay")
    templates = CONST.EndpointTemplates
    return client.APIClient(base_url=base_url, delay=delay, templates=templates)


@pytest.fixture(scope='session')
def field_validator():
    """provides a field validator"""

    return validator.BrewerySchema()


@pytest.fixture(scope='session')
def db():
    """provides an object for working with a database dump"""

    db_obj = dump_db.DumpDB()
    db_obj.load_from_csv(CONST.BACKUP_DB_PATH)
    return db_obj
