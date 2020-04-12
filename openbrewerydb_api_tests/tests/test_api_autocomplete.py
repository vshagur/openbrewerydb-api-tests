import pytest

from openbrewerydb_api_tests import constants as CONST

WORDS = [
    'brewery',
    'fox',
    'ruhstaller%20beer',
    'ruhstaller_beer',
    'san',
    'san%20brewery',
    'wolf',
]


class TestAutocompleteResponse:
    """"""

    @pytest.fixture(scope='class', params=WORDS)
    def dataset(self, request, api_client):
        """returns the result of the request to api"""

        endpoint = CONST.ENDPOINT_TEMPLATES['autocomplete'].format(request.param)
        response = api_client.get(endpoint).json()
        return request.param, response

    def test_response_not_empty(self, dataset):
        """response data is not  empty"""

        word, response = dataset
        assert response

    def test_response_autocomplete_match(self, api_client, dataset):
        """request word occurs in response data"""

        word, response = dataset
        ids = [item['id'] for item in response]

        for id in ids:
            endpoint = CONST.ENDPOINT_TEMPLATES['id'].format(id)
            data = api_client.get(endpoint).json()
            # ignore fields with id
            values = [value for value in data.values() if isinstance(value, str)]

            assert data and filter(lambda x: word in x.lower(), values)
