import pytest

import openbrewerydb_api_tests.constants as CONST

WORDS = [
    'diving',
]


class TestSearchResponse:
    @pytest.fixture(scope='class', params=WORDS)
    def dataset(self, request, api_client):
        """returns the result of the request to api"""

        endpoint = CONST.ENDPOINT_TEMPLATES['search'].format(request.param)
        response = api_client.get(endpoint).json()
        return request.param, response

    def test_response_not_empty(self, dataset):
        """response data is not  empty"""

        word, response = dataset
        assert response

    def test_response_autocomplete_match(self, api_client, dataset):
        """request word occurs in response data"""

        pass  # todo specify search engine requirements


class TestSearchResponseBadValue:
    @pytest.mark.parametrize(
        'value',
        ('53cf66ac', '{}', '%20', ''))
    def test_search_response_bad_value(self, api_client, value):
        """a search request returns an empty list if a bad value is passed"""

        endpoint = CONST.ENDPOINT_TEMPLATES['search'].format(value)
        response = api_client.get(endpoint)
        assert response.json() == []
