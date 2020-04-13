import re

# =======================================================================================
# api section
# =======================================================================================
DEFAULT_URL = 'https://api.openbrewerydb.org/'

DEFAULT_REQUEST_DELAY = 0.1

DEFAULT_NUMBER_PER_PAGE = 20

MAX_NUMBER_PER_PAGE = 50

ENDPOINT_TEMPLATES = {
    'autocomplete': 'breweries/autocomplete?query={}',
    'brewery_type': 'breweries?by_type={}',
    'city': 'breweries?by_city={}',
    'id': 'breweries/{}',
    'name': 'breweries?by_name={}',
    'page': 'breweries?page={}',
    'pages': 'breweries?per_page={}',
    'postal_code': 'breweries?by_postal={}',
    'search': 'breweries/search?query={}',
    'state': 'breweries?by_state={}',
    'tag': 'breweries?by_tag={}',
    'tags': 'breweries?by_tags={}',
}

# =======================================================================================
#  validators section
# =======================================================================================

FIELD_NAMES = [
    'id', 'name', 'brewery_type', 'street', 'city', 'state', 'postal_code', 'country',
    'longitude', 'latitude', 'phone', 'website_url', 'updated_at', 'tag_list'
]

BREWERY_TYPES = [
    'micro', 'regional', 'brewpub', 'large', 'planning', 'bar', 'contract', 'proprietor'
]

TAGS = [
    'dog-friendly', 'patio', 'food-service', 'food-truck', 'tours'
]

COUNTRIES = [
    "United States",
]

USA_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois",
    "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
    "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
    "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
    "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

MAX_LENTH_STRING_FIELD = 80

MIN_LENTH_STRING_FIELD = 0

MIN_LENTH_NAME_FIELD = 3

CITY_REGEX = re.compile(r'([A-Z]{1}[a-z]*)*')

POSTAL_CODE_REGEX = re.compile(r'^\d{5}(-\d{4}){0,4}$')

WEBSITE_REGEX = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

DATETIME_PATTERN = '%Y-%m-%dT%H:%M:%S.%fZ'
# The date format in the database dump is different from the date format in api
DATETIME_PATTERN_DB = '%Y-%m-%d %H:%M:%S.%f'

MAX_LONGITUDE_VALUE = 180.0

MIN_LONGITUDE_VALUE = -180.0

MAX_LATITUDE_VALUE = 90.0

MIN_LATITUDE_VALUE = -90.0

MESSAGE_ERROR_REGEX = re.compile(r"^Couldn't find Brewery with 'id'=.+$")
