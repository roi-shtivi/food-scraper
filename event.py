from util import to_google_format
from datetime import timedelta, datetime


class Event:
    """
    Represnts a calendar event
    """

    def __init__(self, event_institute, title, start_date,
                 end_date, body, location, link, scraper):
        """
        Initializes an event.
        If end_date is missing, it will use start_date + 30 minutes instead.
        """
        if not end_date:
            end_date = start_date + timedelta(minutes=30)
        self.event_institute = event_institute
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.body = body
        self.location = location
        self.link = link
        self.scraped_by = scraper
        self.timestamp = datetime.now()

    def __repr__(self):
        """
        Represntation of an event contains title, start date and location.
        """
        return 'title: ' + self.title + \
            '\nstart_date: ' + str(self.start_date) + \
            '\nlocation: ' + self.location + '\n'

    def to_tuple(self):
        """
        Creates a tuple from the fields of the event.
        """
        return (self.event_institute,
                self.title,
                to_google_format(self.start_date),
                to_google_format(self.end_date),
                self.body,
                self.location,
                self.link,
                self.scraped_by,
                to_google_format(self.timestamp))
