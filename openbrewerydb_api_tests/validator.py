import re

from marshmallow import Schema, fields, validate, ValidationError

from openbrewerydb_api_tests import constants as CONST


def web_site_validator(data):
    """Custom validator for web site field"""

    if data and re.match(CONST.WEBSITE_REGEX, data) is None:
        raise ValidationError("Data not provided.")


class BrewerySchema(Schema):
    id = fields.Int(required=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=CONST.MIN_LENTH_NAME_FIELD,
                                 max=CONST.MAX_LENTH_STRING_FIELD)
    )

    brewery_type = fields.Str(
        required=True,
        validate=validate.OneOf(choices=CONST.BREWERY_TYPES)
    )

    street = fields.Str(
        required=True,
        validate=validate.Length(min=CONST.MIN_LENTH_STRING_FIELD,
                                 max=CONST.MAX_LENTH_STRING_FIELD)
    )

    city = fields.Str(
        required=True,
        allow_none=True,
        validate=validate.Regexp(CONST.CITY_REGEX)
    )

    state = fields.Str(
        required=True,
        allow_none=True,
        validate=validate.OneOf(choices=CONST.USA_STATES)
    )

    postal_code = fields.Str(
        required=True,
        allow_none=True,
        validate=validate.Regexp(CONST.POSTAL_CODE_REGEX)
    )

    country = fields.Str(
        required=True,
        validate=validate.OneOf(choices=CONST.COUNTRIES)
    )

    longitude = fields.Float(
        required=True,
        allow_none=True,
        validate=validate.Range(min=-180, max=180)
        # why does trying to specify values with variables (CONST.MIN_LONGITUDE_VALUE,
        # CONST.MAX_LATITUDE_VALUE) drop tests?
    )

    latitude = fields.Float(
        required=True,
        allow_none=True,
        validate=validate.Range(min=-180, max=180)
        # same question as above
    )

    phone = fields.Str(required=False)

    website_url = fields.Str(
        required=True,
        allow_none=True,
        validate=web_site_validator
    )

    updated_at = fields.DateTime(
        CONST.DATETIME_PATTERN,
        required=True
    )

    tag_list = fields.List(fields.Str(
        required=True,
        validate=validate.OneOf(choices=CONST.TAGS))
    )


class AutocompleteSchema(Schema):
    id = fields.Int(required=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=CONST.MIN_LENTH_NAME_FIELD,
                                 max=CONST.MAX_LENTH_STRING_FIELD)
    )
