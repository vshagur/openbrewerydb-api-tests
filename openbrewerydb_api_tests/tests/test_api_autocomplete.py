import pytest

from openbrewerydb_api_tests import constants as CONST


class TestAutocompleteResponse:
    """"""

    word = None

    @pytest.fixture(scope='class',
                    params=['the_shop', 'san', 'brewery', 'fox', 'wolf', 'san%20brewery'])
    def response(self, request, api_client):
        """returns the result of the request to api"""

        TestAutocompleteResponse.word = request.param
        endpoint = CONST.EndpointTemplates.autocomplete.template.format(self.word)
        yield api_client.get(endpoint)
        self.word = None

    def test_response_autocomplete_status_code(self, response):
        """check status_code"""

        assert response.status_code == 200

    def test_response_autocomplete_count_items(self, response):
        """the number of returned breweries does not exceed 15"""

        assert 0 < len(response.json()) <= 15

    def test_response_autocomplete_field_names(self, response, autocomplete_validator):
        """check format"""

        for brewery_data in response.json():
            errors = autocomplete_validator.validate(brewery_data)
            assert not errors, f'Data format error: {errors}\nData: {brewery_data}\n'

    def test_response_autocomplete_match(self, response, api_client):
        """request word occurs in response data"""

        ids = [item['id'] for item in response.json()]
        for id in ids:
            endpoint = CONST.EndpointTemplates.id.template.format(id)
            new_response = api_client.get(endpoint)

            assert new_response.status_code == 200

            assert new_response.json()

            data = new_response.json()
            values = [value for value in data.values() if isinstance(value, str)]

            assert filter(lambda x: self.word in x.lower(), values)
