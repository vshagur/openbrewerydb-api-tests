import pytest

from openbrewerydb_api_tests import constants as CONST
from openbrewerydb_api_tests import generators


class TestRequestToApiWithErrors:
    @pytest.mark.parametrize('id', ('NotExistID', 10 ** 9, '_', -20))
    def test_get_single_brewery_not_exist_id(self, api_client, id):
        """checking server response with invalid id"""

        endpoint = CONST.EndpointTemplates.single_brewery.template.format(id)
        response = api_client.get(endpoint)
        assert response.status_code == 404
        assert response.json() == {'message': f"Couldn't find Brewery with 'id'={id}"}


class TestFilteredResponseByNotExistValue:
    @pytest.mark.parametrize(
        'value',
        (generators.bad_endpoints_generator(['micro', 'micro micro', 'micro bar'])))
    def test_filter_by_type_bad_value(self, api_client, value):
        """api returns does not return data when an invalid request
        for the brewery_type field"""

        endpoint = CONST.EndpointTemplates.type.template.format(value)
        response = api_client.get(endpoint)
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.parametrize(
        'value',
        (['00000', '00000-0000'] + generators.bad_endpoints_generator(
            ['44107', '45822 45822', '45215 4548'],
            separators=['__', '%20', '.', '--', ''])))
    def test_filter_by_postal_code_bad_value(self, api_client, value):
        """api returns does not return data when an invalid request
        for the postal_code field"""

        endpoint = CONST.EndpointTemplates.code.template.format(value)
        response = api_client.get(endpoint)
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.parametrize(
        'value',
        (generators.bad_endpoints_generator(['Ohio', 'New Mexico', 'Ohio Ohio'])))
    def test_filter_by_state_bad_value(self, api_client, value):
        """api returns does not return data when an invalid request for the state field"""

        endpoint = CONST.EndpointTemplates.state.template.format(value)
        response = api_client.get(endpoint)
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.parametrize(
        'value',
        (generators.bad_endpoints_generator(['Baltimore', 'San Diego', 'Ava Ava'])))
    def test_filter_by_city_bad_value(self, api_client, value):
        """api returns does not return data when an invalid request for the city field"""

        endpoint = CONST.EndpointTemplates.city.template.format(value)
        response = api_client.get(endpoint)
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.parametrize(
        'value',
        (generators.bad_endpoints_generator(['Running Dogs Brewery', 'GBC', 'GBC GBC'])))
    def test_filter_by_name_bad_value(self, api_client, value):
        """api returns does not return data when an invalid request for the name field"""

        endpoint = CONST.EndpointTemplates.name.template.format(value)
        response = api_client.get(endpoint)
        assert response.status_code == 200
        assert response.json() == []
