import pytest

from openbrewerydb_api_tests import constants as CONST

endpoints = [
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
]


@pytest.mark.parametrize('sign', ['', '-']) # todo добавить "+",
#  если он предусматривался требованиями к api
@pytest.mark.parametrize('endpoint', endpoints)
@pytest.mark.parametrize('field',
                         [field for field in CONST.FIELD_NAMES if field != 'tag_list'])
def test_field_sorting(api_client, sign, field, endpoint):
    """check sorting"""

    reverse = True if sign == '-'  else False
    response = api_client.get(f'{endpoint}&sort={sign}{field}')

    assert response.status_code == 200

    fields = [item[field] for item in response.json() if item[field]]

    assert 0 <= len(fields) <= 20

    assert fields == sorted(fields, reverse=reverse)
