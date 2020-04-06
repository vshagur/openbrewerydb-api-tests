import pytest

from openbrewerydb_api_tests import constants as CONST


class TestAutocompleteResponse:
    @pytest.fixture(scope='class', params=['san', 'brewery', 'fox', 'wolf'])
    def response(self, request, api_client):
        """returns the result of the request to api"""

        endpoint = CONST.EndpointTemplates.autocomplete.template.format(request.param)
        return api_client.get(endpoint)

    def test_response_autocomplete_status_code(self, response):
        """check status_code"""

        assert response.status_code == 200

    def test_response_autocomplete_count_fields(self, response):
        """the number of returned breweries does not exceed 15"""

        assert 0 <= len(response.json()) <= 15

    def test_response_autocomplete_field_names(self, response, autocomplete_validator):
        """check format"""

        for brewery_data in response.json():
            errors = autocomplete_validator.validate(brewery_data)
            assert not errors, f'Data format error: {errors}\nData: {brewery_data}\n'
