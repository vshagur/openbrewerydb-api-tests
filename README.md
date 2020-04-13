# openbrewerydb-api-tests
Test suite for Open Brewery DB API (https://www.openbrewerydb.org/).

## Table of contents
* [General info](#general-info)
* [Installation](#installation)
* [Run tests](#run-tests)

## General info
The openbrewerydb-api-tests project provides several test suites for api [https://www.openbrewerydb.org/)](https://www.openbrewerydb.org/). The project is based on the [pytest](https://docs.pytest.org/en/latest/contents.html) framework with the pytest-html plugin. To validate the data, the [marshmallow](https://marshmallow.readthedocs.io/en/stable/index.html) library is used. API requests are sent using the [requests](https://requests.readthedocs.io/en/master/) library.
 

## Installation
    $ git clone git@github.com:vshagur/openbrewerydb-api-tests.git
    $ cd openbrewerydb-api-tests/
    $ python3.6 -m venv .env
    $ source .env/bin/activate
    $ pip install pip --upgrade
    $ pip install -r requirements.txt
    
## Run tests
    
    $ python -m pytest --html=report.html  --url="https://api.openbrewerydb.org/" --delay=0.1 openbrewerydb_api_tests/

Keys: 

    --delay - the delay between requests to the server,     
    --html - the file with test results, 
    --url - the base URL (you can run tests on a local server)
