#!/usr/bin/env bash

python -m pytest --html=reports/autocomplete_report.html openbrewerydb_api_tests/tests/test_api_autocomplete.py
python -m pytest --html=reports/base_report.html openbrewerydb_api_tests/tests/test_api_base.py
python -m pytest --html=reports/filter_report.html openbrewerydb_api_tests/tests/test_api_filter.py
python -m pytest --html=reports/search_report.html openbrewerydb_api_tests/tests/test_api_search.py
python -m pytest --html=reports/sorting_report.html openbrewerydb_api_tests/tests/test_api_sorting.py
