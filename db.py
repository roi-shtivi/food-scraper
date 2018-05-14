import sqlite3
from util import *

def save_events_to_db(events, existing_db, new_db):
    events_conn = sqlite3.connect(existing_db)
    new_conn = sqlite3.connect(new_db)
    events_cur = events_conn.cursor()
    new_cur = new_conn.cursor()
    new_cur.execute(
        '''CREATE table IF NOT EXISTS events (event_institute text, title text, start_date text, end_date text, body text, location text, link text)''')
    events_cur.execute(
        '''CREATE table IF NOT EXISTS events (event_institute text, title text, start_date text, end_date text, body text, location text, link text)''')

    new_events = 0

    for event in events:
        not_exists = events_cur.execute('SELECT * FROM events WHERE title=? AND start_date=? AND location=?', (
        event.title, to_google_format(event.start_date), event.location)).fetchone() == None

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
        'start': {'dateTime': e[2],
                  'timeZone': 'Asia/Jerusalem'},
        'end': {'dateTime': e[3],
                'timeZone': 'Asia/Jerusalem'},
    } for e in events]
    return json_events