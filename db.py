import sqlite3
from util import to_google_format


def save_events_to_db(events, existing_db, new_db):
    """
    Saves a list of events to the filenames existing_db and new_db.
    This function creates the events table if it is missing from the file.
    """
    events_conn = sqlite3.connect(existing_db)
    new_conn = sqlite3.connect(new_db)
    events_cur = events_conn.cursor()
    new_cur = new_conn.cursor()
    new_cur.execute(
        '''CREATE table IF NOT EXISTS events
        (event_institute text,
        title text,
        start_date text,
        end_date text,
        body text,
        location text,
        link text,
        scraped_by text,
        timestamp text)
        '''
    )
    events_cur.execute(
        '''CREATE table IF NOT EXISTS events
        (event_institute text,
        title text,
        start_date text,
        end_date text,
        body text,
        location text,
        link text,
        scraped_by text,
        timestamp text)
        '''
    )

    new_events = 0

    for event in events:
        not_exists = events_cur.execute(
            '''SELECT * FROM events
            WHERE title=? AND start_date=? AND location=?
            ''', (
                event.title,
                to_google_format(event.start_date),
                event.location)).fetchone() is None

        if not_exists:
            events_cur.execute(
                '''INSERT INTO events
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                event.to_tuple())
            new_cur.execute(
                '''INSERT INTO events
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                event.to_tuple())
            new_events += 1

    events_conn.commit()
    new_conn.commit()
    print("{} events were added to {}".format(new_events, new_db))
    return new_events


def db_to_json(db_file):
    """
    Converts a db file to JSON of events.
    """

    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    events = c.execute('SELECT * FROM events').fetchall()
    json_events = [{
        'summary': e[1],
        'description': event_description(e),
        "location": e[5],  # free form
        'start': {'dateTime': e[2],
                  'timeZone': 'Asia/Jerusalem'},
        'end': {'dateTime': e[3],
                'timeZone': 'Asia/Jerusalem'},
    } for e in events]
    return json_events


def event_description(event):
    """
    Creates a string that describes the event.
    """
    inst = 'institute: ' + event[0] + '\n' if event[0] else ''
    return inst + '{}\n{}'.format(event[4], event[6])
