import re
import urllib.parse

import pytest

import openbrewerydb_api_tests.constants as CONST

VALUES = {
    'brewery_type': CONST.BREWERY_TYPES,
    'tag': CONST.TAGS,
    'state': CONST.USA_STATES,
    'city': ['Arrington',
             'Ballston Lake',
             'Bay Shore',
             'Elizaville',
             'Greensboro',
             'Lino Lakes',
             'Manassas',
             'Maple Grove',
             'New York',
             'Pisgah Forest',
             'Portland',
             'Rochester',
             'Rocky Point',
             'Saint Clair Shores',
             'South Lyon',
             'Winchester',
             'Winston Salem'],
    'name': ['beer',
             'beer company',
             'big',
             'brewery',
             'city food',
             'company',
             'gordon biersch',
             'granite city food',
             'northwest',
             'red truck beer',
             'restaurant',
             'washington',
             'west'],
    'tags': [
        'patio dog-friendly'
    ],
    'postal_code': [
        '15301',
        '15301-4912',
        '16335',
        '16335-3432',
        '28806',
        '44107',
        '44107-4840',
        '49286',
        '49286-1553',
        '55369',
        '55369-3629',
        '55746',
        '55746-1713',
        '80513',
        '82801',
        '82801-3619',
        '95565'],
}


class TestFilteredResponse:
    """"""

    def is_all_fields_valid(self, field_name, response, func):
        """Returns True if the list of fields is not empty and a call to funс for all
        elements returns True"""

        fields = [item[field_name] for item in response.json()]
        return fields and all(map(func, fields))

    @pytest.mark.parametrize('value', VALUES['brewery_type'])
    def test_filter_by_type(self, api_client, value):
        """check filtering by type of brewery"""

        response = api_client.get_filter_by('brewery_type', value)
        assert self.is_all_fields_valid('brewery_type', response, lambda x: x == value)

    @pytest.mark.parametrize('value', filter(lambda x: not x.count(' '), VALUES['city']))
    def test_filter_by_city(self, api_client, value):
        """check filtering by city (single-word city name)"""

        response = api_client.get_filter_by('city', value.lower())
        assert self.is_all_fields_valid('city', response, lambda x: x == value)

    @pytest.mark.parametrize('value', filter(lambda x: x.count(' '), VALUES['city']))
    def test_filter_by_city_percent_coding_url(self, api_client, value):
        """check filtering by city (percent coding url)"""

        new_value = urllib.parse.quote(value.lower())
        response = api_client.get_filter_by('city', new_value)
        assert self.is_all_fields_valid('city', response, lambda x: x == value)

    @pytest.mark.parametrize('value', filter(lambda x: x.count(' '), VALUES['city']))
    def test_filter_by_city_underline_coding_url(self, api_client, value):
        """check filtering by city (underline coding url)"""

        new_value = value.lower().replace(' ', '_')
        response = api_client.get_filter_by('city', new_value)
        assert self.is_all_fields_valid('city', response, lambda x: x == value)

    @pytest.mark.parametrize('value', filter(lambda x: not x.count(' '), VALUES['name']))
    def test_filter_by_name(self, api_client, value):
        """check filtering by name (single-word brewery name)"""

        response = api_client.get_filter_by('name', value.lower())
        assert self.is_all_fields_valid(
            'name', response, lambda x: value.lower() in x.lower())

    @pytest.mark.parametrize('value', filter(lambda x: x.count(' '), VALUES['name']))
    def test_filter_by_name_underline_coding_url(self, api_client, value):
        """check filtering by name (underline coding url)"""

        new_value = value.lower().replace(' ', '_')
        response = api_client.get_filter_by('name', new_value)
        assert self.is_all_fields_valid(
            'name', response, lambda x: value.lower() in x.lower())

    @pytest.mark.parametrize('value', filter(lambda x: x.count(' '), VALUES['name']))
    def test_filter_by_name_percent_coding_url(self, api_client, value):
        """check filtering by name (percent coding url)"""

        new_value = urllib.parse.quote(value.lower())
        response = api_client.get_filter_by('name', new_value)
        assert self.is_all_fields_valid(
            'name', response, lambda x: value.lower() in x.lower())

    @pytest.mark.skip(reason='This is a work in progress. The production database does '
                             'not yet have many tags associated with breweries.')
    @pytest.mark.parametrize('value', VALUES['tag'])
    def test_filter_by_tag(self, api_client, value):
        """check filtering by tag"""

        response = api_client.get_filter_by('tag', value.lower())
        assert self.is_all_fields_valid('tag_list', response, lambda x: value in x)

    @pytest.mark.skip(reason='This is a work in progress. The production database does '
                             'not yet have many tags associated with breweries.')
    @pytest.mark.parametrize('value', VALUES['tags'])
    def test_filter_by_tags(self, api_client, value):
        """check filtering by tags"""

        new_value = ','.join(value.split())
        response = api_client.get_filter_by('tags', new_value)
        for tag in value.split():
            assert self.is_all_fields_valid('tag_list', response, lambda x: tag in x)

    @pytest.mark.parametrize('value', filter(lambda x: not x.count(' '), VALUES['state']))
    def test_filter_by_state(self, api_client, value):
        """check filtering by state (single-word state name)"""

        response = api_client.get_filter_by('state', value.lower())
        assert self.is_all_fields_valid('state', response, lambda x: x == value)

    @pytest.mark.parametrize('value',
                             filter(lambda x: x.count(' '), VALUES['state']))
    def test_filter_by_state_percent_coding_url(self, api_client, value):
        """check filtering by state (percent coding url)"""

        new_value = urllib.parse.quote(value.lower())
        response = api_client.get_filter_by('state', new_value)
        assert self.is_all_fields_valid('state', response, lambda x: x == value)

    @pytest.mark.parametrize('value', filter(lambda x: x.count(' '), VALUES['state']))
    def test_filter_by_state_underline_coding_url(self, api_client, value):
        """check filtering by state (underline coding url)"""

        new_value = value.lower().replace(' ', '_')
        response = api_client.get_filter_by('state', new_value)
        assert self.is_all_fields_valid('state', response, lambda x: x == value)

    @pytest.mark.parametrize(
        'value',
        filter(lambda x: len(x) == 5, VALUES['postal_code']))
    def test_filter_by_basic_postal_code(self, api_client, value):
        """check filtering by basic (5 digit) postal code"""

        regex = re.compile('^' + value + '(-\\d{4}){0,4}$')
        response = api_client.get_filter_by('postal_code', value)
        assert self.is_all_fields_valid(
            'postal_code', response, lambda x: bool(re.match(regex, x)))

    @pytest.mark.parametrize(
        'value',
        filter(lambda x: len(x) == 10, VALUES['postal_code']))
    def test_filter_by_postal_code(self, api_client, value):
        """check filtering by basic postal+4 (9 digit) """

        response = api_client.get_filter_by('postal_code', value)
        assert self.is_all_fields_valid('postal_code', response, lambda x: x == value)

    @pytest.mark.parametrize(
        'value',
        filter(lambda x: len(x) == 10, VALUES['postal_code']))
    def test_filter_by_postal_code_underline(self, api_client, value):
        """check filtering by basic postal+4 (9 digit), underline separator """

        new_value = value.replace('-', '_')
        response = api_client.get_filter_by('postal_code', value)
        assert self.is_all_fields_valid('postal_code', response, lambda x: x == value)


class TestNumberPerPage:
    @pytest.mark.parametrize('number', (0, 1, 2, 19, 20, 21, 49, 50))
    def test_number_elements_per_page(self, api_client, number):
        """checking the number of elements per page"""

        endpoint = CONST.ENDPOINT_TEMPLATES['pages'].format(number)
        response = api_client.get(endpoint)
        assert len(response.json()) == number

    @pytest.mark.parametrize('number', (-51, -50, -49, -21, -20, -19, -1))
    def test_number_elements_per_page_negative_value(self, api_client, number):
        """checking the number of elements per page (negative values)"""

        endpoint = CONST.ENDPOINT_TEMPLATES['pages'].format(number)
        response = api_client.get(endpoint)
        assert len(response.json()) == 0

    @pytest.mark.parametrize('number', (51, 100, 500, 1000))
    def test_number_elements_per_page_more_than_maximum(self, api_client, number):
        """checking the number of elements per page (value > 50)"""

        endpoint = CONST.ENDPOINT_TEMPLATES['pages'].format(number)
        response = api_client.get(endpoint)
        assert len(response.json()) == CONST.MAX_NUMBER_PER_PAGE
