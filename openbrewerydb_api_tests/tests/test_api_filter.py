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

    @pytest.mark.parametrize('number', ('%20', 'one'))
    def test_number_elements_per_page_not_valid_value(self, api_client, number):
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

    @pytest.mark.parametrize('number', (1, 2, 19, 20, 21, 49, 50, 51, 223))
    def test_number_elements_for_page(self, api_client, number):
        """checking the number of elements per page (page request)"""

        endpoint = CONST.ENDPOINT_TEMPLATES['page'].format(number)
        response = api_client.get(endpoint)
        assert len(response.json()) == CONST.DEFAULT_NUMBER_PER_PAGE

    @pytest.mark.parametrize('number', (0, -1, -2, 1000, 'one', '%20'))
    def test_number_elements_for_page_not_valid_value(self, api_client, number):
        """checking the number of elements per page (page request)"""

        endpoint = CONST.ENDPOINT_TEMPLATES['page'].format(number)
        response = api_client.get(endpoint)
        assert len(response.json()) == 0


class TestFilteredResponseBadValue:
    """"""

    @pytest.mark.parametrize(
        'value',
        ('53cf66ac', '{}', 'running__dogs__brewery', 'running%20%20dogs%20%20brewery',
         'running.dogs.brewery', 'running-dogs-brewery', 'runningdogsbrewery',
         '%20brewery', 'modern,times', '%20', '%20running%20dogs%20brewery'))
    def test_filter_by_name_bad_value(self, api_client, value):
        """a request by the name field filter returns an empty list if a bad value
        is passed"""

        response = api_client.get_filter_by('name', value)
        assert response.json() == []

    @pytest.mark.parametrize(
        'value',
        ('4002f33a', '{}', 'san__diego', 'san%20%20diego', 'san.diego', 'san-diego',
         'sandiego', 'ava__ava', 'ava%20%20ava', 'ava.ava', 'ava-ava', 'avaava',
         'febaltimore', 'baltimorewk', '123456789', '%20new%20york', 'ne_york',
         'new,york', '%20'))
    def test_filter_by_city_bad_value(self, api_client, value):
        """a request by the city field filter returns an empty list if a bad value
        is passed"""

        response = api_client.get_filter_by('city', value)
        assert response.json() == []

    # todo узнать про поиск, так как "tex" вернет для texas
    @pytest.mark.parametrize(
        'value',
        ('80b5b388', '{}', 'new__mexico', 'new%20%20mexico', 'new.mexico', 'new-mexico',
         'newmexico', 'ohio__ohio', 'ohio%20%20ohio', 'ohio.ohio', 'ohio-ohio',
         'ohioohio', 'knohio', 'ohiouf''%20texas', 'new,mexico', '%20'))
    def test_filter_by_state_bad_value(self, api_client, value):
        """a request by the state field filter returns an empty list if a bad value
        is passed"""

        response = api_client.get_filter_by('state', value)
        assert response.json() == []

    @pytest.mark.parametrize(
        'value',
        ('00000', '00000-0000', 'TBD', 'cea8d6ce', '{}', '45822__45822', '45822%2045822',
         '45822.45822', '45822--45822', '4582245822', '45215__4548', '45215%204548',
         '45215.4548', '45215--4548', '452154548', 'tn44107', '44107jv', '%2044107',
         '45215,4548', '%20'))
    def test_filter_by_postal_code_bad_value(self, api_client, value):
        """a request by the postal_code field filter returns an empty list if a bad value
        is passed"""

        response = api_client.get_filter_by('postal_code', value)
        assert response.json() == []

    @pytest.mark.parametrize(
        'value',
        ('5962bbcb', '{}', 'micro__micro', 'micro%20%20micro', 'micro.micro',
         'micro-micro', 'micromicro', 'micro__bar', 'micro%20%20bar', 'micro.bar',
         'micro-bar', 'microbar', 'fumicro', 'microms', '%20micro', '%20', 'micro,bar'))
    def test_filter_by_type_bad_value(self, api_client, value):
        """a request by the brewery_type field filter returns an empty list if
        a bad value is passed"""

        response = api_client.get_filter_by('brewery_type', value)
        assert response.json() == []
        # todo проверить разделитель запятая, на некоторых запроса может проходить

    @pytest.mark.skip(reason='little data, not implemented')
    def test_filter_by_tag_value(self, api_client, value):
        """"""  # todo
        pass

    @pytest.mark.skip(reason='little data, not implemented')
    def test_filter_by_tags_value(self, api_client, value):
        """"""  # todo
        pass
