from util import to_google_format
from datetime import timedelta
import util


class Event:
    """
    Represents a calendar event
    """

    def __init__(self, event_institute, title, start_date,
                 end_date, body, location, link):
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

    def __repr__(self):
        """
        Representation of an event contains title, start date and location.
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
                self.link)

    def location_label(self):
        location_tokens = self.location.replace(',', '').split(' ')
        # 2 words match
        for i in range(len(location_tokens) - 1):
            word, word2 = location_tokens[i:i+2]
            try:
                value = util.places[word[0].upper()]
            except (KeyError, IndexError):
                continue
            for place in value:
                if (word + " " + word2) in place:
                    return place
        # 1 word match
        for word in location_tokens:
            try:
                value = util.places[word[0].upper()]
            except (KeyError, IndexError):
                continue
            for place in value:
                if word in place:
                    return place
        return None

    def __lt__(self, other):
        """
        Standard order by start date
        """
        return self.start_date < other.start_date

    def __eq__(self, other):
        if isinstance(other, Event):
            return self.start_date == other.start_date and \
                    self.location_label() == other.location_label()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.start_date, self.location_label()))


if __name__ == '__main__':
    a = Event("", "", 1, " ", "", "Seminar Hall, Dancinger A (Chemistry) Building ", None)
    b = Event("", "", 1, " ", "", "Seminar Hall, Dancinger A (Chemistry) Building ", None)
    j = {a, b}
    print(j)
