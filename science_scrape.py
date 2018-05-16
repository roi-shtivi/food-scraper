from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import util
import db
from event import Event

# css labels contained in the table row
css_labels = [
    'field-event-institute',
    'title',
    'field-start-date',
    'body',
    'field-location',
    'event-link']


def get_events():
    """
    Returns a list of events from the address:
    'http://science.huji.ac.il/en/events new'
    """
    url = 'http://science.huji.ac.il/en/events new'
    raw_html = util.simple_get(url)

    if raw_html is None:
        print('Could not get url')
        return None

    html = BeautifulSoup(raw_html, 'html.parser')
    events = []
    for i in range(1, 4):
        table = '.view-display-id-block_{}'.format(i)
        trs = html.select(table)[0].find_all('tr')
        for tr in trs[1:]:
            events.append(get_event_from_tr(tr))

    print('obtained {} events from {}'.format(len(events), url))
    return events


def get_event_from_tr(tr):
    """
    Returns an event from a table row
    """
    event_institute = try_to_get_css(tr, css_labels[0])
    title = try_to_get_css(tr, css_labels[1])
    start_date = parse_datetime(try_to_get_css(tr, css_labels[2]))
    body = try_to_get_css(tr, css_labels[3])
    location = try_to_get_css(tr, css_labels[4])
    link = try_to_get_css(tr, css_labels[5])
    return Event(event_institute, title, start_date,
                 None,  body, location, link)


def try_to_get_css(tr, field):
    """
    Returns the stripped text of a specific field of a specific table row.
    If an error is encountered, will return an empty string.
    """
    try:
        return tr.select('.views-field-' + field)[0].text.strip()
    except IndexError:
        return ''


def parse_datetime(str_date):
    """
    Parses a date string, typically found in this website.
    Returns a datetime.
    """
    try:
        return datetime.strptime(str_date, '%A, %b %d, %Y - %H:%M')
    except BaseException:
        return None


if __name__ == '__main__':
    events = get_events()
    num = db.save_events_to_db(events, 'events.db', 'new_events.db')
