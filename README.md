# openbrewerydb-api-tests
Test suite for Open Brewery DB API (https://www.openbrewerydb.org/).

## Table of contents
* [General info](#general-info)
* [Installation](#installation)
* [Run tests](#run-tests)

## General info
The openbrewerydb-api-tests project provides several test suites for api [https://www.openbrewerydb.org/)](https://www.openbrewerydb.org/). The project is based on the [pytest](https://docs.pytest.org/en/latest/contents.html) framework with the pytest-html plugin. To validate the data, the [marshmallow](https://marshmallow.readthedocs.io/en/stable/index.html) library is used. API requests are sent using the [requests](https://requests.readthedocs.io/en/master/) library.
 

## Installation
Clone the project and go inside the project directory.

    $ git clone git@github.com:vshagur/openbrewerydb-api-tests.git
    $ cd openbrewerydb-api-tests/
    
Create a virtual environment.

    $ python3.6 -m venv .env
    $ source .env/bin/activate
    
Install the dependencies.

    $ pip install pip --upgrade
    $ pip install -r requirements.txt
    
## Run tests
#### Testing the basic functionality of API.
The test suite checks the main characteristics of the api response - status response code, headers, response format. This test suite can be used as a smoke test.

    $ python -m pytest openbrewerydb_api_tests/tests/test_api_base.py

The project defines additional command line interface options. You can set a delay between requests and specify the api address.

Keys: 

    --delay - the delay between requests to the server,     
    --url - the base URL (you can run tests on a local server)
    
To save the test report in the html file, use the key:

    --html - the file with test results
    
An example of running tests using parameters:


    $ python -m pytest --html=report.html  --url="https://api.openbrewerydb.org/" --delay=0.1 openbrewerydb_api_tests/tests/test_api_base.py
    
    
#### Testing API responses to requests using data filtering options.
Validating data filtering in API responses.

    $ python -m pytest --html=report.html  --url="https://api.openbrewerydb.org/" --delay=0.1 openbrewerydb_api_tests/tests/test_api_filter.py
    
    
#### Testing API responses to search queries.
Validation of API responses to search queries.   
    
    $ python -m pytest --html=report.html  --url="https://api.openbrewerydb.org/" --delay=0.1 openbrewerydb_api_tests/tests/test_api_search.py
    
    
#### Testing API responses to requests by passing sorting parameters.
The test suite checks API sorting functionality.

    $ python -m pytest --html=report.html  --url="https://api.openbrewerydb.org/" --delay=0.1 openbrewerydb_api_tests/tests/test_api_sorting.py
    
    
#### Testing API responses to autocompletion requests.
Check API completion capabilities.

    $ python -m pytest --html=report.html  --url="https://api.openbrewerydb.org/" --delay=0.1 openbrewerydb_api_tests/tests/test_api_autocomplete.py
    
## Authors

* **Valeriy Shagur**  - [vshagur](https://github.com/vshagur), email: vshagur@gmail.com

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/vshagur/exgrex/blob/master/LICENSE) file for details    
