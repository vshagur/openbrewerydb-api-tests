from collections import namedtuple

DEFAULT_URL = 'https://api.openbrewerydb.org/'

DEFAULT_REQUEST_DELAY = 1

BREWERY_TYPES = [
    'micro', 'regional', 'brewpub', 'large', 'planning', 'bar', 'contract', 'proprietor'
]

TAGS = ['dog-friendly', 'patio', 'food-service', 'food-truck', 'tours']

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


class EndpointTemplates:
    Templates = namedtuple('Templates', ('field_name, template'))

    type = Templates('brewery_type', 'breweries?by_type={}')
    city = Templates('city', 'breweries?by_city={}')
    name = Templates('name', 'breweries?by_name={}')
    tag = Templates('tag_list', 'breweries?by_tag={}')
    tags = Templates('tag_list', 'breweries?by_tags={}')
    state = Templates('state', 'breweries?by_state={}')
    code = Templates('postal_code', 'breweries?by_postal={}')
    id = Templates('id', 'breweries/{}')
