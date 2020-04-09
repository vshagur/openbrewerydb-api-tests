import pytest

# =======================================================================================
# Test data
# =======================================================================================
ENDPOINTS = {
    'TestListResponse': [
        'breweries?by_city=portland',
        'breweries?by_city=san_diego',
        'breweries?by_city=new%20york',
        'breweries?by_name=cooper',
        'breweries?by_name=craft_brewery'
        'breweries?by_name=modern%20times',
        'breweries?by_state=ohio',
        'breweries?by_name=new_york',
        'breweries?by_name=new%20mexico',
        'breweries?by_postal=44107',
        'breweries?by_postal=04103-1072',
        'breweries?by_postal=95112_5932',
        'breweries?by_type=micro',
        'breweries?by_tag=patio',
        'breweries?by_tags=patio,dog-friendly',  # failed
        'breweries?page=15',
        'breweries?per_page=25',
        'breweries?by_state=ohio&sort=type',
        'breweries?by_state=ohio&sort=-name',
        'breweries?by_state=new%20york&sort=+id'
    ],
    'TestGetResponse': [
        'breweries/1',
        'breweries/3417',
        'breweries/8000',
    ],
    'TestSearchResponse': [
        'breweries/search?query=dog',
        'breweries/search?query=red_bank',
        'breweries/search?query=red%20bank',
    ],
    'TestAutocompleteResponse': [
        'breweries/autocomplete?query=texas',
        'breweries/autocomplete?query=company%20brewery',
        'breweries/autocomplete?query=company_brewery',
    ],
    'TestRequestWithMessageErrors': [
        'breweries/not_exist',
        'breweries/9999999999',
        'breweries/_',
        'breweries/-20',
        'breweries/0',
        'breweries/%20'
    ]
}


# =======================================================================================
# Tests
# =======================================================================================

class TestListResponse:
    """"""  # todo

    @pytest.fixture(scope='class', params=ENDPOINTS['TestListResponse'])
    def response(self, api_client, request):
        """return response"""

        return api_client.get(request.param)

    def test_response_code(self, response):
        """check response code"""

        assert response.status_code == 200

    def test_headers_content_type(self, response):
        """check content_type"""

        assert response.headers['Content-type'] == 'application/json; charset=utf-8'

    def test_responses_data_not_empty(self, response):
        """check responses is not empty"""

        assert response.json()

    def test_responses_format(self, response, fields_validator):
        """check responses format"""

        for brewery_data in response.json():
            errors = fields_validator.validate(brewery_data)
            assert not errors, f'Data format error: {errors}\nData: {brewery_data}\n'


class TestGetResponse:
    """"""  # todo

    @pytest.fixture(scope='class', params=ENDPOINTS['TestGetResponse'])
    def response(self, api_client, request):
        """return response"""

        return api_client.get(request.param)

    def test_response_code(self, response):
        """check response code"""

        assert response.status_code == 200

    def test_headers_content_type(self, response):
        """check content_type"""

        assert response.headers['Content-type'] == 'application/json; charset=utf-8'

    def test_responses_data_not_empty(self, response):
        """check responses is not empty"""

        assert response.json()

    def test_responses_format(self, response, fields_validator):
        """check responses format"""

        data = response.json()
        errors = fields_validator.validate(data)
        assert not errors, f'Data format error: {errors}\nData: {data}\n'


class TestSearchResponse:
    """"""  # todo

    @pytest.fixture(scope='class', params=ENDPOINTS['TestSearchResponse'])
    def response(self, api_client, request):
        """return response"""

        return api_client.get(request.param)

    def test_response_code(self, response):
        """check response code"""

        assert response.status_code == 200

    def test_headers_content_type(self, response):
        """check content_type"""

        assert response.headers['Content-type'] == 'application/json; charset=utf-8'

    def test_responses_data_not_empty(self, response):
        """check responses is not empty"""

        assert response.json()

    def test_responses_format(self, response, fields_validator):
        """check responses format"""

        for brewery_data in response.json():
            errors = fields_validator.validate(brewery_data)
            assert not errors, f'Data format error: {errors}\nData: {brewery_data}\n'


class TestAutocompleteResponse:
    """"""  # todo

    @pytest.fixture(scope='class', params=ENDPOINTS['TestAutocompleteResponse'])
    def response(self, api_client, request):
        """return response"""

        return api_client.get(request.param)

    def test_response_code(self, response):
        """check response code"""

        assert response.status_code == 200

    def test_headers_content_type(self, response):
        """check content_type"""

        assert response.headers['Content-type'] == 'application/json; charset=utf-8'

    def test_responses_data_not_empty(self, response):
        """check responses is not empty"""

        assert response.json()

    def test_responses_format(self, response, fields_short_validator):
        """check responses format"""

        for brewery_data in response.json():
            errors = fields_short_validator.validate(brewery_data)
            assert not errors, f'Data format error: {errors}\nData: {brewery_data}\n'


class TestRequestWithMessageErrors:
    """"""  # todo

    @pytest.fixture(scope='class', params=ENDPOINTS['TestRequestWithMessageErrors'])
    def response(self, api_client, request):
        """return response"""
        return api_client.get(request.param)

    def test_response_code(self, response):
        """check response code"""

        assert response.status_code == 404

    def test_headers_content_type(self, response):
        """check content_type"""

        assert response.headers['Content-type'] == 'application/json; charset=utf-8'

    def test_responses_data_not_empty(self, response):
        """check responses is not empty"""

        assert response.json()

    def test_responses_format(self, response):
        """check responses format"""

        data = response.json()
        assert 'message' in data.keys() and len(data.keys()) == 1
