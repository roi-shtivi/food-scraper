import sqlite3
from util import to_google_format


class Db:
    """
    Interacts with a DB file for events.
    """

    def __init__(self, db_file_name):
        """
        :param db_file_name: database file
        """
        self.file_name = db_file_name
        self.conn = sqlite3.connect(db_file_name)
        self.cur = self.conn.cursor()
        self.cur.execute(
            '''CREATE table IF NOT EXISTS events
            (event_institute text,
            title text,
            start_date text,
            end_date text,
            body text,
            location text,
            link text)
            '''
        )

    def save_events_to_db(self, events):
        """
        Saves a list of events to the filenames existing_db and new_db.
        This function creates the events table if it is missing from the file.
        """
        for event in events:
            self.cur.execute(
                '''INSERT INTO events
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                event.to_tuple())

        self.conn.commit()
        print("{} events were added to {}".format(len(events), self.file_name))

    def to_json(self):
        """
        Converts a db file to JSON of events.
        """
        events = self.cur.execute('SELECT * FROM events').fetchall()
        json_events = [{
            'summary': e[1],
            'description': event_description(e),
            "location": e[5],  # free form
            'start': {'dateTime': e[2], 'timeZone': 'Asia/Jerusalem'},
            'end': {'dateTime': e[3], 'timeZone': 'Asia/Jerusalem'},
        } for e in events]
        return json_events

    def remove_existing_events_from_list(self, events):
        """
        Returns a list from the events in the param events which are not in
        the database.
        """
        new_events = []

        for event in events:
            not_exists = self.cur.execute(
                '''SELECT * FROM events
                WHERE title=? AND start_date=? AND location=?
                ''', (
                    event.title,
                    to_google_format(event.start_date),
                    event.location)).fetchone() is None

            if not_exists:
                new_events.append(event)
        return new_events


def event_description(event):
    """
    Creates a string that describes the event.
    """
    inst = 'institute: ' + event[0] + '\n' if event[0] else ''
    return inst + '{}\n{}'.format(event[4], event[6])
