import re
import time

import pytest

from openbrewerydb_api_tests import constants as CONST


def test_unique_id(db):
    """check that id is not repeated"""

    fields = db.select_fields('id')
    assert len(fields) == len(set(fields))


class TestBackupDB:
    """validation of fields in the database"""

    @pytest.fixture(scope='class',
                    params=range(1, CONST.NUMBER_DB_RECORDS + 1),
                    ids=lambda param: f'record in database with id: {param}')
    def item(self, request, db):
        """return database record with id==param """

        return db.select_items('id', lambda x: x == request.param).pop()

    def test_brewery_type_fields(self, item):
        """check brewery_type field"""

        value = item['brewery_type']
        assert value == '' or value in CONST.BREWERY_TYPES

    def test_postal_code_fields(self, item):
        """check postal_code field"""

        value = item['postal_code']
        assert value == '' or re.match(CONST.POSTAL_CODE_REGEX, value)

    def test_name_fields(self, item):
        """check name field"""

        value = item['name']
        assert CONST.MIN_LENTH_NAME_FIELD <= len(value) <= \
               CONST.MAX_LENTH_STRING_FIELD

    def test_city_fields(self, item):
        """check city field"""

        value = item['city']
        assert re.match(CONST.CITY_REGEX, value)

    def test_street_fields(self, item):
        """check street field"""

        value = item['street']
        assert CONST.MIN_LENTH_STRING_FIELD <= len(value) <= \
               CONST.MAX_LENTH_STRING_FIELD

    def test_state_type_fields(self, item):
        """check state field"""

        value = item['state']
        assert value == '' or value in CONST.USA_STATES

    def test_country_type_fields(self, item):
        """check country field"""

        value = item['country']
        assert value == '' or value in CONST.COUNTRIES

    def test_longitude_fields(self, item):
        """check longitude field"""

        value = item['longitude']
        assert value == '' or CONST.MIN_LONGITUDE_VALUE <= float(value) <= \
                              CONST.MAX_LONGITUDE_VALUE

    def test_latitude_fields(self, item):
        """check latitude field"""

        value = item['latitude']
        assert value == '' or CONST.MIN_LATITUDE_VALUE <= float(value) <= \
                              CONST.MAX_LATITUDE_VALUE

    def test_website_url_fields(self, item):
        """check website_url field"""

        value = item['website_url']
        assert value == '' or re.match(CONST.WEBSITE_REGEX, value)

    def test_updated_at_fields(self, item):
        """check updated_at field"""

        value = item['updated_at']
        try:
            time.strptime(value, CONST.DATETIME_PATTERN_DB)
        except:
            assert False

    def test_lenth_phone_fields(self, item):
        """check lenth of phone field"""

        value = item['phone']
        assert value == '' or 8 < len(value) < 11

    def test_phone_fields(self, item):
        """phone field is number"""

        value = item['phone']
        assert value == '' or value.isdigit()

    @pytest.mark.skip(reason='this field is not in the database dump')
    def test_tag_list_fields(self, item):
        """check phone tag_list field"""

        value = item['tag_list']
        assert True  # todo write a test condition
