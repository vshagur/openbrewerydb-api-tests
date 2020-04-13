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
        'breweries?by_name=craft_brewery',
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
        'breweries?by_state=new%20york&sort=+id',
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
    """the class provides a set of tests for answering requests with filtering by field,
    the basic parameters are checked - the response code, headers, the presence of data
    in the response and the compliance of the data with the format"""

    @pytest.fixture(scope='class', params=ENDPOINTS['TestListResponse'])
    def response(self, api_client, request):
        """fixture sends a request to api, returns a response object"""

        return api_client.get(request.param)

    def test_response_code(self, response):
        """check status response code"""

        assert response.status_code == 200

    def test_headers_content_type(self, response):
        """check content_type"""

        assert response.headers['Content-type'] == 'application/json; charset=utf-8'

    def test_responses_data_not_empty(self, response):
        """check responses is not empty"""

        assert response.json()

    def test_response_autocomplete_count_items(self, response):
        """the number of returned items does not exceed 15"""

        assert 0 < len(response.json()) <= 20

    def test_responses_format(self, response, fields_validator):
        """check responses format"""

        for brewery_data in response.json():
            errors = fields_validator.validate(brewery_data)
            assert not errors, f'Data format error: {errors}\nData: {brewery_data}\n'


class TestGetResponse:
    """the class provides a set of tests for answering requests with filtering by ID,
    the basic parameters are checked - the response code, headers, the presence of data
    in the response and the compliance of the data with the format"""

    @pytest.fixture(scope='class', params=ENDPOINTS['TestGetResponse'])
    def response(self, api_client, request):
        """fixture sends a request to api, returns a response object"""

        return api_client.get(request.param)

    def test_response_code(self, response):
        """check status response code"""

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
    """the class provides a set of tests for answering search queries, the basic
    parameters are checked - the response code, headers, the presence of data in the
    response and the compliance of the data with the format"""

    @pytest.fixture(scope='class', params=ENDPOINTS['TestSearchResponse'])
    def response(self, api_client, request):
        """return response"""

        return api_client.get(request.param)

    def test_response_code(self, response):
        """check status response code"""

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
    """the class provides a set of tests for answering autocomplete requests, the basic
    parameters are checked - the response code, headers, number of items returned,
    the presence of data in the response and the compliance of the data with the format"""

    @pytest.fixture(scope='class', params=ENDPOINTS['TestAutocompleteResponse'])
    def response(self, api_client, request):
        """fixture sends a request to api, returns a response object"""

        return api_client.get(request.param)

    def test_response_code(self, response):
        """check status response code"""

        assert response.status_code == 200

    def test_headers_content_type(self, response):
        """checking response headers"""

        assert response.headers['Content-type'] == 'application/json; charset=utf-8'

    def test_responses_data_not_empty(self, response):
        """check that the content of the response is not empty"""

        assert response.json()

    def test_response_autocomplete_count_items(self, response):
        """the number of returned items does not exceed 15"""

        assert 0 < len(response.json()) <= 15

    def test_responses_format(self, response, fields_short_validator):
        """checking the format of the content of the response"""

        for brewery_data in response.json():
            errors = fields_short_validator.validate(brewery_data)
            assert not errors, f'Data format error: {errors}\nData: {brewery_data}\n'


class TestRequestWithMessageErrors:
    """the class provides a set of tests for responding to requests that receive an
    error message, the basic parameters are checked - the response code, headers,
    the presence of data in the response and the compliance of the data with the format"""

    @pytest.fixture(scope='class', params=ENDPOINTS['TestRequestWithMessageErrors'])
    def response(self, api_client, request):
        """fixture sends a request to api, returns a response object"""
        return api_client.get(request.param)

    def test_response_code(self, response):
        """check status response code"""

        assert response.status_code == 404

    def test_headers_content_type(self, response):
        """check content_type"""

        assert response.headers['Content-type'] == 'application/json; charset=utf-8'

    def test_responses_data_not_empty(self, response):
        """check responses is not empty"""

        assert response.json()

    def test_responses_format(self, response, message_error_validator):
        """check responses format"""

        data = response.json()
        errors = message_error_validator.validate(data)
        assert not errors, f'Data format error: {errors}\nData: {data}\n'
