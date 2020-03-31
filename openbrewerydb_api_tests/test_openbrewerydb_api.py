import urllib.parse
from itertools import combinations

import pytest

from openbrewerydb_api_tests import constants


# =======================================================================================
# Tests
# =======================================================================================


class TestGetResponse:
    ENDPOINTS = [
        'breweries?by_city=san_diego',
        'breweries?by_city=san%20diego',
        'breweries?by_name=cooper',
        'breweries?by_name=modern%20times',
        'breweries?by_state=ohio',
        'breweries?by_name=new_york',
        'breweries?by_name=new%20mexico',
        'breweries?by_postal=44107',
        'breweries?by_postal=44107-4020',
        'breweries?by_postal=44107_4020',
        'breweries?by_type=micro',
        'breweries?by_tag=patio',
        'breweries?page=15',
        'breweries?per_page=25',
        'breweries?by_state=ohio&sort=type,-name',
        'breweries?by_city=san_diego&sort=-name',
    ]

    @pytest.fixture(scope='class', params=ENDPOINTS)
    def response(self, api_client, request):
        """return response"""

        return api_client.get(request.param)

    def test_response_code(self, response):
        """check response code"""

        assert response.status_code == 200

    def test_headers_content_type(self, response):
        """check content_type"""

        assert response.headers['Content-type'] == 'application/json; charset=utf-8'

    def test_responses_format(self, response, field_validator):
        """check responses format"""

        for brewery_data in response.json():
            errors = field_validator.validate(brewery_data)
            assert not errors, f'Data format error: {errors}\nData: {brewery_data}\n'


class TestFilteredResponse:
    def is_all_fields_valid(self, field_name, response, func):
        """Returns True if the call of function func on all elements of the fields
        returns True."""

        fields = [item[field_name] for item in response.json()]
        return all(map(func, (field for field in fields)))

    @pytest.mark.parametrize('value', constants.BREWERY_TYPES)
    def test_filter_by_type(self, api_client, value):
        """check filtering by type of brewery"""

        field_name = constants.EndpointTemplates.type.field_name
        response = api_client.get_filter_by('type', value)
        assert self.is_all_fields_valid(field_name, response, lambda x: x == value)

    @pytest.mark.parametrize(
        'value',
        ('Rochester', 'Saint Clair Shores', 'South Lyon', 'Lino Lakes', 'Maple Grove',
         'Manassas', 'Winchester', 'Arrington',))
    def test_filter_by_city_percent_coding_url(self, api_client, value):
        """check filtering by city (percent coding url)"""

        new_value = urllib.parse.quote(value.lower())
        field_name = constants.EndpointTemplates.city.field_name
        response = api_client.get_filter_by('city', new_value)
        assert self.is_all_fields_valid(field_name, response, lambda x: x == value)

    @pytest.mark.parametrize(
        'value',
        ('Pisgah Forest', 'Winston Salem', 'Bay Shore', 'New York', 'Ballston Lake',
         'Rocky Point', 'Elizaville', 'Greensboro',))
    def test_filter_by_city_underline_coding_url(self, api_client, value):
        """check filtering by city (underline coding url)"""

        new_value = value.lower().replace(' ', '_')
        field_name = constants.EndpointTemplates.city.field_name
        response = api_client.get_filter_by('city', new_value)
        assert self.is_all_fields_valid(field_name, response, lambda x: x == value)

    @pytest.mark.parametrize(
        'value',
        ('big', 'brewery', 'company', 'beer company', 'red truck beer', 'company',
         'beer',))
    def test_filter_by_name_underline_coding_url(self, api_client, value):
        """check filtering by name (underline coding url)"""

        new_value = value.replace(' ', '_')
        field_name = constants.EndpointTemplates.name.field_name
        response = api_client.get_filter_by('name', new_value)
        assert self.is_all_fields_valid(
            field_name, response, lambda x: value in x.lower())

    @pytest.mark.parametrize(
        'value',
        ('city food', 'granite city food', 'restaurant', 'gordon biersch', 'west',
         'northwest', 'washington',))
    def test_filter_by_name_percent_coding_url(self, api_client, value):
        """check filtering by name (percent coding url)"""

        new_value = urllib.parse.quote(value.lower())
        field_name = constants.EndpointTemplates.name.field_name
        response = api_client.get_filter_by('name', new_value)
        assert self.is_all_fields_valid(
            field_name, response, lambda x: value in x.lower()
        )

    @pytest.mark.parametrize('value', constants.TAGS)
    def test_filter_by_tag(self, api_client, value):
        """check filtering by tag"""

        field_name = constants.EndpointTemplates.tag.field_name
        response = api_client.get_filter_by('tag', value)
        assert self.is_all_fields_valid(field_name, response, lambda x: value in x)

    @pytest.mark.parametrize('value', constants.USA_STATES[::2])
    def test_filter_by_state_percent_coding_url(self, api_client, value):
        """check filtering by state (percent coding url)"""

        field_name = constants.EndpointTemplates.state.field_name
        new_value = urllib.parse.quote(value.lower())
        response = api_client.get_filter_by('state', new_value)
        assert self.is_all_fields_valid(field_name, response, lambda x: x == value)

    @pytest.mark.parametrize('value', constants.USA_STATES[1::2])
    def test_filter_by_state_underline_coding_url(self, api_client, value):
        """check filtering by state (underline coding url)"""

        field_name = constants.EndpointTemplates.state.field_name
        new_value = value.lower().replace(' ', '_')
        response = api_client.get_filter_by('state', new_value)
        assert self.is_all_fields_valid(field_name, response, lambda x: x == value)

    @pytest.mark.parametrize('value1, value2', list(combinations(constants.TAGS, 2)))
    def test_filter_by_tags(self, api_client, value1, value2):
        """check filtering by tags"""

        field_name = constants.EndpointTemplates.tags.field_name
        new_value = ','.join((value1, value2))
        response = api_client.get_filter_by('tags', new_value)
        assert self.is_all_fields_valid(
            field_name, response, lambda x: value1 in x and value2 in x
        )

    @pytest.mark.parametrize(
        'value',
        ('44107', '49286', '95565', '55746', '55369', '82801', '16335', '15301',))
    def test_filter_by_basic_postal_code(self, api_client, value):
        """check filtering by basic (5 digit) postal code"""

        field_name = constants.EndpointTemplates.code.field_name
        response = api_client.get_filter_by('code', value)
        assert self.is_all_fields_valid(
            field_name, response, lambda x: x.startswith(value)
        )

    @pytest.mark.parametrize(
        'value',
        ('44107-4840', '49286-1553', '55746-1713', '55369-3629', '82801-3619',
         '16335-3432', '15301-4912',))
    def test_filter_by_postal_code(self, api_client, value):
        """check filtering by basic postal+4 (9 digit) """

        field_name = constants.EndpointTemplates.code.field_name
        response = api_client.get_filter_by('code', value)
        assert self.is_all_fields_valid(
            field_name, response, lambda x: x.startswith(value)
        )

    @pytest.mark.parametrize(
        'value',
        ('44107_4840', '49286_1553', '55746_1713', '55369_3629', '82801_3619',
         '16335_3432', '15301_4912',))
    def test_filter_by_postal_code_underline(self, api_client, value):
        """check filtering by basic postal+4 (9 digit), underline"""

        field_name = constants.EndpointTemplates.code.field_name
        response = api_client.get_filter_by('code', value)
        assert self.is_all_fields_valid(
            field_name, response, lambda x: x == value.replace('_', '-')
        )


class TestNumberPerPage:
    @pytest.mark.parametrize('number', (0, 1, 2, 19, 20, 21, 49, 50))
    def test_number_elements_per_page(self, api_client, number):
        """checking the number of elements per page"""

        endpoint = constants.EndpointTemplates.per_page.template.format(number)
        response = api_client.get(endpoint)
        assert len(response.json()) == number

    @pytest.mark.parametrize('number', (-51, -50, -49, -21, -20, -19, -1))
    def test_number_elements_per_page_negative_value(self, api_client, number):
        """checking the number of elements per page (negative values)"""

        endpoint = constants.EndpointTemplates.per_page.template.format(number)
        response = api_client.get(endpoint)
        assert len(response.json()) == constants.DEFAULT_NUMBER_PER_PAGE

    @pytest.mark.parametrize('number', (51, 100, 1000))
    def test_number_elements_per_page_negative_value(self, api_client, number):
        """checking the number of elements per page (value > 50)"""

        endpoint = constants.EndpointTemplates.per_page.template.format(number)
        response = api_client.get(endpoint)
        assert len(response.json()) == constants.MAX_NUMBER_PER_PAGE