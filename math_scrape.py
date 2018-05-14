from bs4 import BeautifulSoup
import datetime
from datetime import datetime
import util
from event import Event

html_tags = ['.event-year', '.event-start-month', '.event-start-day', '.date-display-start', '.date-display-end',
             '.node-title', '.field-item', '.node-content']


def get_events(url):
    raw_html = util.simple_get(url)

    if raw_html == None:
        print('Could not get url')
        return None

    i = 2
    html = BeautifulSoup(raw_html, 'html.parser')
    events = []
    container = html.select('.views-row-1')
    while container:
        event = get_event_from_container(container[0])
        if event:
            events.append(event)
        container = html.select('.views-row-{}'.format(i))
        i += 1
    print('obtained {} events from {}'.format(len(events), url))
    return events


def get_event_from_container(container):
    title = try_to_get_css(container, html_tags[5])
    if not title or 'TBA' in title:  # if the event is not complete in the site or to be announce.
        return None

    location = container.select('.field-items')[1].text.strip()
    link = container.find('a')['href']
    sub_container = BeautifulSoup(util.simple_get(link), 'html.parser')
    body = try_to_get_css(sub_container, html_tags[7])  # body is obtained from another link ('link')

    # get time elements
    t = get_time_elements(container)

    # construct time strings
    str_s_date = t['year'] + ' ' + t['month'] + ' ' + t['day'] + ' ' + t['s_hour']
    str_e_date = t['year'] + ' ' + t['month'] + ' ' + t['day'] + ' ' + t['e_hour']

    # parse the string time
    s_date = parse_datetime(str_s_date)
    e_date = parse_datetime(str_e_date)

    return Event('Einstein Institute of Mathematics', title, s_date, e_date, body, location, link)


def get_time_elements(container):
    year = try_to_get_css(container, html_tags[0])
    month = try_to_get_css(container, html_tags[1])
    day = try_to_get_css(container, html_tags[2])
    s_hour = try_to_get_css(container, html_tags[3])
    e_hour = try_to_get_css(container, html_tags[4])
    return {'year': year, 'month': month, 'day': day, 's_hour': s_hour, 'e_hour': e_hour}


def parse_datetime(str_date):
    try:
        return datetime.strptime(str_date, '%Y %B %d %I:%M%p')
    except:
        return None


def try_to_get_css(container, field):
    try:
        return container.select(field)[0].text.strip()
    except IndexError:
        return ''


if __name__ == '__main__':
    now = datetime.now()
    two_digit_month = '{:02d}'.format(now.month)
    url = 'http://mathematics.huji.ac.il/calendar/upcoming/eventss/events-seminars?type=month&month=' + str(
        now.year) + '-' + two_digit_month
    print(get_events(url))
