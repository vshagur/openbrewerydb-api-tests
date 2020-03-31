from marshmallow import Schema, fields, validate

from openbrewerydb_api_tests import constants


class BrewerySchema(Schema):
    id = fields.Int(required=True)

    name = fields.Str(required=True)

    brewery_type = fields.Str(required=True,
                              validate=validate.OneOf(choices=constants.BREWERY_TYPES))

    street = fields.Str(required=True)

    city = fields.Str(required=True,
                      allow_none=True,
                      validate=validate.Regexp(r'([A-Z]{1}[a-z]*)*'))

    state = fields.Str(required=True,
                       allow_none=True)

    postal_code = fields.Str(required=True,
                             allow_none=True,
                             validate=validate.Regexp(r'^\d{5}(-\d{4}){0,4}$'))

    country = fields.Str(required=True)

    longitude = fields.Float(required=True,
                             allow_none=True,
                             validate=validate.Range(-180.0, 180.0))

    latitude = fields.Float(required=True,
                            allow_none=True,
                            validate=validate.Range(-90.0, 90.0))

    phone = fields.Str(required=False)

    website_url = fields.Str(required=True,
                             allow_none=True)

    updated_at = fields.DateTime('%Y-%m-%dT%H:%M:%S.%fZ',
                                 required=True, )

    tag_list = fields.List(fields.Str(validate=validate.OneOf(choices=constants.TAGS)),
                           required=True)
