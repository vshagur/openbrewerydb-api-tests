import re

from marshmallow import Schema, fields, validate, ValidationError

from openbrewerydb_api_tests import constants

website_regex = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

city_regex = re.compile(r'([A-Z]{1}[a-z]*)*')

postal_code_regex = re.compile(r'^\d{5}(-\d{4}){0,4}$')


def web_site_validator(data):
    """Custom validator for web site field"""
    if data and re.match(website_regex, data) is None:
        raise ValidationError("Data not provided.")


class BrewerySchema(Schema):
    id = fields.Int(required=True)

    name = fields.Str(required=True, validate=validate.Length(min=3, max=80))

    brewery_type = fields.Str(required=True,
                              validate=validate.OneOf(choices=constants.BREWERY_TYPES))

    street = fields.Str(required=True,
                        validate=validate.Length(min=0, max=80))

    city = fields.Str(required=True,
                      allow_none=True,
                      validate=validate.Regexp(city_regex))

    state = fields.Str(required=True,
                       allow_none=True,
                       validate=validate.OneOf(choices=constants.USA_STATES))

    postal_code = fields.Str(required=True,
                             allow_none=True,
                             validate=validate.Regexp(postal_code_regex))

    country = fields.Str(required=True,
                         validate=validate.OneOf(choices=constants.COUNTRIES))

    longitude = fields.Float(required=True,
                             allow_none=True,
                             validate=validate.Range(-180.0, 180.0))

    latitude = fields.Float(required=True,
                            allow_none=True,
                            validate=validate.Range(-90.0, 90.0))

    phone = fields.Str(required=False)

    website_url = fields.Str(required=True,
                             allow_none=True,
                             validate=web_site_validator)

    updated_at = fields.DateTime('%Y-%m-%dT%H:%M:%S.%fZ',
                                 required=True, )

    tag_list = fields.List(fields.Str(validate=validate.OneOf(choices=constants.TAGS)),
                           required=True)
