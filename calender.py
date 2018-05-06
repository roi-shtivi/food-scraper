from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import os
import scrape



SCOPES = 'https://www.googleapis.com/auth/calendar'  # read&write permissions
CALENDER_ID = 'mail.huji.ac.il_ohkpphph8fngk46dtjj0hk9ams@group.calendar.google.com' # FFF
# CALENDER_ID = '45qti41i2evvupo6tubj5upm78@group.calendar.google.com' # ROI

# example event
EVENTS = [{
    'summary': 'Test',
    'description': 'Good food wow',
    "location": 'Danciger B',  # free form
    'start':  {'dateTime': '2018-05-06T13:00:00',
               'timeZone': 'Asia/Jerusalem'},
    'end':    {'dateTime': '2018-05-06T16:00:00',
               'timeZone': 'Asia/Jerusalem'},
}]

changes = {
    'summary': 'patched_Test'
}


def setup():
    """
    create calender
    :return: google calender object
    """
    try:
	    if not os.path.exists('storage.json'):
	        open('storage.json', "w+")
	    store = file.Storage('storage.json')
	    creds = store.get()
	    if not creds or creds.invalid:
	        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
	        creds = tools.run_flow(flow, store)  # ask to auth
	    g_cal = discovery.build('calendar', 'v3', http=creds.authorize(Http()))
	    return g_cal
    except Exception  as err:
    	print('google calendar object was not initialize successfully')
    	return None


def print_status(e):
    """
    Print the status of an event
    :param e: Event object
    :return:
    """
    print('''*** %r event added:
        Start: %s
        End:   %s''' % (e['summary'].encode('utf-8'),
                        e['start']['dateTime'], e['end']['dateTime']))


def add_events(g_cal, events, cal_id):
    """
    add events to g_cal calender
    :param g_cal: google calender object
    :param events: list of Events
    :return: list of the
    """
    try:
	    added = []
	    for event in events:
	        e = g_cal.events().insert(calendarId=cal_id,
	                             sendNotifications=False, body=event).execute()
	        added.append(e)
	        print_status(e)
	    return added
    except Exception as err:
    	print('Event was not created successfully')
    	return None


def delete_event(g_cal, event_id, cal_id):
    g_cal.events().delete(calendarId=cal_id, eventId=event_id).execute()


if __name__ == "__main__":
	g_cal = setup()
        events = get_events()
        num = save_events_to_db(events, 'events.db', 'new_events.db')
	added = add_events(g_cal, scrape.db_to_json('new_events.db'), CALENDER_ID)

