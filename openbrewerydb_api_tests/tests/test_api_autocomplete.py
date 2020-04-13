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


class TestAutocompleteResponseBadValue:
    @pytest.mark.parametrize(
        'value',
        ('53cf66ac', '{}', 'running__dogs__brewery', 'running%20%20dogs%20%20brewery',
         'running.dogs.brewery', 'running-dogs-brewery', 'runningdogsbrewery',
         '%20brewery', 'modern,times', '%20', '%20running%20dogs%20brewery', ''))
    def test_autocomplete_response_bad_value(self, api_client, value):
        """a autocomplete request returns an empty list if a bad value is passed"""

        endpoint = CONST.ENDPOINT_TEMPLATES['autocomplete'].format(value)
        response = api_client.get(endpoint)
        assert response.json() == []
