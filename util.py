from requests import get
from requests.exceptions import RequestException
from contextlib import closing

EXAMPLE_EVENTS = [{
    'summary': 'Test',
    'description': 'Good food wow',
    "location": 'Danciger B',  # free form
    'start': {'dateTime': '2018-05-06T13:00:00',
              'timeZone': 'Asia/Jerusalem'},
    'end': {'dateTime': '2018-05-06T16:00:00',
            'timeZone': 'Asia/Jerusalem'},
}]

# keep it sorted by len can be done by sort_dict()
places = {
    'A': ['Academon', 'Alberman', 'Aronberg', 'Amphitheater'],
    'B': ['Berman', 'Bergman', 'Brandman', 'Brickman'],
    'C': ['Canada', 'Casali', 'Cosell'],
    'D': ['Daroff', 'Dvorsky', 'Dancinger', 'Dancinger A', 'Dancinger B', 'Dormitories'],
    'E': ['Earth'],
    'F': ['Feldman'],
    'G': ['Geology'],
    'H': ['Harman', 'Hakiria'],
    'I': [],
    'J': [],
    'K': ['Kaplun'],
    'L': ['Levy', 'Levin', 'Lubin', 'Libermann', 'Los Angeles'],
    'M': ['Marks', 'Manchester', 'Mathematics', 'Maison de France'],
    'N': [],
    'O': ['ORT'],
    'P': ['Planetarium', 'Philadelphia'],
    'Q': [],
    'R': ['Ross', 'Rubin', 'Rothberg'],
    'S': ['Sherman', 'Sprinzak', 'Silberman', 'Silverman'],
    'T': ['Taylor'],
    'U': [],
    'V': [],
    'W': ['Weissman', 'Wolffsohn'],
    'X': [],
    'Y': [],
    'Z': []
}


def sort_dict():
    for key in places.keys():
        places[key].sort(key=lambda item: len(item))


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def to_google_format(date_time):
    """
    Formats a given datetime to the format required by google calendar.
    """
    try:
        return date_time.strftime('%Y-%m-%dT%H:%M:%S')
    except BaseException:
        return ''
