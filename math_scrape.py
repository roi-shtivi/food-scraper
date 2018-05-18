from bs4 import BeautifulSoup
import datetime
from datetime import datetime
import util
from event import Event
import re

css_tags = [
    '.event-year',
    '.event-start-month',
    '.event-start-day',
    '.date-display-start',
    '.date-display-end',
    '.node-title',
    '.field-item',
    '.node-content']


def get_events(url):
    """
    :param url: the url address to scrape events from
    :return: Return a list of Event
    """
    raw_html = util.simple_get(url)
    if raw_html is None:
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
    """
    Extract the event detail from the css event container
    :param container: beautiful soup Tag object
    :return: Event objects corresponding to the container data.
    """
    try:
        title = try_to_get_css(container, css_tags[5])
        # if the event is not complete in the site or to be announce.
        if not title or 'TBA' in title:
            return None
        try:
            location = container.select('.field-items')[1].text.strip()
        # no location has found
        except IndexError:
            return None
        link = container.find('a')['href']
        sub_container = BeautifulSoup(util.simple_get(link), 'html.parser')
        # body is obtained from another link ('link')
        body = try_to_get_css(sub_container, css_tags[7])

        # get time elements
        t = get_time_elements(container)
        if t is None:
            return None

        # construct time strings
        str_s_date = t['year'] + ' ' + t['month'] + ' ' + t['day'] + ' ' + t[
            's_hour']
        str_e_date = t['year'] + ' ' + t['month'] + ' ' + t['day'] + ' ' + t[
            'e_hour']

        # parse the string time
        s_date = parse_datetime(str_s_date)
        e_date = parse_datetime(str_e_date)

        return Event(
            'Einstein Institute of Mathematics',
            title,
            s_date,
            e_date,
            body,
            location,
            link)
    except Exception:
        return None


def get_time_elements(container):
    """
    Extract the event time data from the css event container
    :param container: beautiful soup Tag object
    :return: dictionary of time attributes
    """
    year = try_to_get_css(container, css_tags[0])
    month = try_to_get_css(container, css_tags[1])
    day = try_to_get_css(container, css_tags[2])
    # check for all-day event (currently no such supporting yet.)
    if re.search('All day', container.text, re.IGNORECASE):
        return None
    s_hour = try_to_get_css(container, css_tags[3])
    e_hour = try_to_get_css(container, css_tags[4])
    return {
        'year': year,
        'month': month,
        'day': day,
        's_hour': s_hour,
        'e_hour': e_hour}


def parse_datetime(str_date):
    """
    Parse the time that was extract from url format into datetime object
    :param str_date: url's time format
    :return: datetime object
    """
    try:
        return datetime.strptime(str_date, '%Y %B %d %I:%M%p')
    except:
        return None


def try_to_get_css(container, field):
    """
    Try to extract text data from the filed in the the container
    :param container: beautiful soup Tag object
    :param field: text id that represent the specific Tag that the text can be
        found in
    :return: string of the field Tag
    """
    try:
        return container.select(field)[0].text.strip()
    except IndexError:
        return ''


if __name__ == '__main__':
    # print the list of Events that was scraped from the url.
    now = datetime.now()
    two_digit_month = '{:02d}'.format(now.month)
    url = 'http://mathematics.huji.ac.il/calendar/upcoming/eventss/events' \
          '-seminars?type=month&month=' + str(now.year) + '-' + two_digit_month
    print(get_events(url))
