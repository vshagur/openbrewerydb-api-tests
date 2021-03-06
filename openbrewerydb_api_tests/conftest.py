import pytest

from openbrewerydb_api_tests import configuration as CONF
from openbrewerydb_api_tests.tools import client
from openbrewerydb_api_tests.tools import dump_db
from openbrewerydb_api_tests.tools import validator


# =======================================================================================
# CLI options
# =======================================================================================
def pytest_addoption(parser):
    """adds command line options"""

    parser.addoption(
        '--url',
        action='store',
        default=CONF.DEFAULT_URL,
        help=f'Base URL for API, by default - {CONF.DEFAULT_URL}.'
    )

    parser.addoption(
        '--delay',
        action='store',
        type=int,
        default=CONF.DEFAULT_REQUEST_DELAY,
        help=f'Delay between API requests, by default - {CONF.DEFAULT_REQUEST_DELAY}.'
    )


# =======================================================================================
# Fixtures
# =======================================================================================
@pytest.fixture(scope="session")
def api_client(request):
    """provides a client for working with api"""

    base_url = request.config.getoption("--url")
    delay = request.config.getoption("--delay")
    templates = CONF.ENDPOINT_TEMPLATES
    return client.APIClient(base_url=base_url, delay=delay, templates=templates)


@pytest.fixture(scope='session')
def fields_validator():
    """provides a field validator"""

    return validator.BrewerySchema()


@pytest.fixture(scope='session')
def fields_short_validator():
    """provides a short fields validator"""

    return validator.ShortBrewerySchema()


@pytest.fixture(scope='session')
def message_error_validator():
    """provides a message error validator"""

    return validator.MessageErrorSchema()


@pytest.fixture(scope='session')
def db():
    """provides an object for working with a database dump"""

    db_obj = dump_db.DumpDB()
    db_obj.load_from_csv(CONF.BACKUP_DB_PATH)
    return db_obj
