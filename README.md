# test-openbrewerydb-api
Test suite for Open Brewery DB API (https://www.openbrewerydb.org/).

#### Installation
    $ git clone git@github.com:vshagur/openbrewerydb-api-tests.git
    $ cd openbrewerydb-api-tests/
    $ python3.6 -m venv .env
    $ source .env/bin/activate
    $ pip install pip --upgrade
    $ pip install -r requirements.txt
    
#### Run tests
    $ python -m pytest --html=report.html  --url="https://api.openbrewerydb.org/" --delay=0.1 openbrewerydb_api_tests/

Keys: 

"--delay" - the delay between requests to the server, 

"--html" - the file with test results, 

"--url" - the base URL
