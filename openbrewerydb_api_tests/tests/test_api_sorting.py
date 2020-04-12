from itertools import product

import pytest

from openbrewerydb_api_tests import constants as CONST

TEST_DATA = {
    'endpoints': [
        # city endpoints
        'breweries?by_city=portland',
        'breweries?by_city=san%20diego',
        'breweries?by_city=san_diego',
        # name endpoints
        'breweries?by_name=company',
        'breweries?by_name=gordon_biersch',
        'breweries?by_name=granite%20city',
        # state endpoints
        'breweries?by_state=california',
        'breweries?by_state=new_york',
        'breweries?by_state=north%20carolina',
        # postal code endpoints
        'breweries?by_postal=44107',
        'breweries?by_postal=44107-4020',
        'breweries?by_postal=44107_4020',
        # type endpoints
        'breweries?by_type=planning',
        # todo add data
    ],
    'fields': [field for field in CONST.FIELD_NAMES if field != 'tag_list'],
    'signs': ['', '-', '+'],
}


class TestSortingResponse:
    """the class provides a set of tests for checking the correctness of sorting
    in api responses and invariance of returned data"""

    @pytest.fixture(
        scope='class',
        params=product(TEST_DATA['endpoints'], TEST_DATA['signs'], TEST_DATA['fields'], ))
    def dataset(self, api_client, request):
        endpoint, sign, field = request.param
        reverse = True if sign == '-' else False
        response = api_client.get(endpoint).json()
        new_endpoint = f'{endpoint}&sort={sign}{field}'
        response_sort = api_client.get(new_endpoint).json()
        return reverse, field, response, response_sort, new_endpoint

    def test_field_sorting(self, dataset):
        """check sorting"""

        reverse, field, _, response_sort, endpoint = dataset
        # Note - ignore empty lines and None
        fields = [item[field] for item in response_sort if item[field]]

        if field == 'id':
            expected = sorted(fields, reverse=reverse, key=lambda x: int(x))
        if field in ('longitude', 'latitude'):
            expected = sorted(fields, reverse=reverse, key=lambda x: float(x))
        else:
            expected = sorted(fields, reverse=reverse)

        assert fields == expected, f'endpoint: {endpoint}\nfields: {fields}\n'

    def test_data_persistence(self, dataset):
        """check data persistence"""

        reverse, field, response, response_sort, endpoint = dataset
        fields = [item['id'] for item in response]
        fields_sort = [item['id'] for item in response_sort]

        assert set(fields) == set(fields_sort), \
            f'endpoint: {endpoint}\nfields: {fields}\n'



        # todo сортировка по не существующему полю, как должно отвечать api?
