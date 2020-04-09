# openbrewerydb-api-tests
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

    --delay - the delay between requests to the server,     
    --html - the file with test results, 
    --url - the base URL (you can run tests on a local server)



новый план
1. smoke tests - проверка работы аpi, проверяем код ответа, заголовок и формат ответа 
(три теста для списка, для get, для автокомплит, и для отсутствующего id (негативный),
для сортировки)
2. проверяем контент - сортировка(количество результатов, правильность сортировки, 
неизменяемость объектов до и после)
3. проверяем контент - фильтрация (количество результатов, правильность)
4. проверяем контент - автокомплит (количество результатов,)