from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import sqlite3

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


class Event:
    def __init__(self, event_institute, title, start_date, body, location, link):
        self.event_institute = event_institute
        self.title = title
        self.start_date = start_date
        self.end_date = start_date + timedelta(minutes=30)
        self.body = body
        self.location = location
        self.link = link

    def __repr__(self):
        return 'title: ' + self.title + '\nstart_date: ' + str(self.start_date) + '\nlocation: ' + self.location + '\n'

    def to_tuple(self):
        return (self.event_institute, self.title, to_google_format(self.start_date), to_google_format(self.end_date), self.body, self.location, self.link)

def get_events():
    url = 'http://science.huji.ac.il/en/events new'
    raw_html = simple_get(url)

    if raw_html == None:
        print('Could not get url')
        return None;

    html = BeautifulSoup(raw_html, 'html.parser')
    events = []
    for i in range(1,4):
        table = '.view-display-id-block_{}'.format(i)
        trs = html.select(table)[0].find_all('tr')
        for tr in trs[1:]:
            events.append(get_event_from_tr(tr))

    print('obtained {} events from {}'.format(len(events), url))
    return events

css_labels = ['field-event-institute', 'title', 'field-start-date', 'body', 'field-location', 'event-link']
def get_event_from_tr(tr):
    event_institute = try_to_get_css(tr, css_labels[0])
    title = try_to_get_css(tr, css_labels[1])
    start_date = parse_datetime(try_to_get_css(tr, css_labels[2]))
    body = try_to_get_css(tr, css_labels[3])
    location = try_to_get_css(tr, css_labels[4])
    link = try_to_get_css(tr, css_labels[5])
    return Event(event_institute ,title, start_date, body, location, link)

def try_to_get_css(tr, field):
    try:
        return tr.select('.views-field-' + field)[0].text.strip()
    except IndexError:
        return ''

def parse_datetime(str_date):
    try:
        return datetime.strptime(str_date, '%A, %b %d, %Y - %H:%M')
    except:
        return None

def to_google_format(date_time):
    try:
        return date_time.strftime('%Y-%m-%dT%H:%M:%S')
    except:
        return ''

def save_events_to_db(events, existing_db, new_db):
    events_conn = sqlite3.connect(existing_db)
    new_conn = sqlite3.connect(new_db)
    events_cur = events_conn.cursor()
    new_cur = new_conn.cursor()
    new_cur.execute('''CREATE table IF NOT EXISTS events (event_institute text, title text, start_date text, end_date text, body text, location text, link text)''')
    events_cur.execute('''CREATE table IF NOT EXISTS events (event_institute text, title text, start_date text, end_date text, body text, location text, link text)''')

    new_events = 0

    for event in events:
        not_exists = events_cur.execute('SELECT * FROM events WHERE title=? AND start_date=? AND location=?', (event.title, to_google_format(event.start_date), event.location)).fetchone() == None
        
        if not_exists:
            events_cur.execute('INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?)', event.to_tuple())
            new_cur.execute('INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?)', event.to_tuple())
            new_events += 1

    events_conn.commit()
    new_conn.commit()
    print("{} events were added to {}".format(new_events, new_db))
    return new_events

def db_to_json(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    events = c.execute('SELECT * FROM events').fetchall()
    json_events = [{
        'summary': e[1],
        'description': ('institute: ' + e[0] + '\n' if e[0] else '') + '{}\n{}'.format(e[4], e[6]),
        "location": e[5],  # free form
        'start':  {'dateTime': e[2],
                   'timeZone': 'Asia/Jerusalem'},
        'end':    {'dateTime': e[3],
                   'timeZone': 'Asia/Jerusalem'},
    } for e in events]
    return json_events




if __name__ == '__main__':
    events = get_events()
    num = save_events_to_db(events, 'events.db', 'new_events.db')

