from util import *

class Event:
    def __init__(self, event_institute, title, start_date, end_date, body, location, link):
        self.event_institute = event_institute
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.body = body
        self.location = location
        self.link = link

    def __repr__(self):
        return 'title: ' + self.title + '\nstart_date: ' + str(self.start_date) + '\nlocation: ' + self.location + '\n'

    def to_tuple(self):
        return (
            self.event_institute, self.title, to_google_format(self.start_date), to_google_format(self.end_date),
            self.body,
            self.location, self.link)