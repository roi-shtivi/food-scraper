from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import os
import scrape

EVENTS = [{
    'summary': 'Test',
    'description': 'Good food wow',
    "location": 'Danciger B',  # free form
    'start': {'dateTime': '2018-05-06T13:00:00',
              'timeZone': 'Asia/Jerusalem'},
    'end': {'dateTime': '2018-05-06T16:00:00',
            'timeZone': 'Asia/Jerusalem'},
}]


class Calendar:
    SCOPES = 'https://www.googleapis.com/auth/calendar'  # read&write permissions
    # CALENDER_ID = 'mail.huji.ac.il_ohkpphph8fngk46dtjj0hk9ams@group.calendar.google.com' #FFF
    CALENDER_ID = '45qti41i2evvupo6tubj5upm78@group.calendar.google.com'  # ROI

    def __init__(self):
        self.g_cal = self.setup()

    def setup(self):
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
                flow = client.flow_from_clientsecrets('client_secret.json', self.SCOPES)
                creds = tools.run_flow(flow, store)  # ask to auth
            g_cal = discovery.build('calendar', 'v3', http=creds.authorize(Http()))
            return g_cal
        except Exception  as err:
            print('google calendar object was not initialize successfully')
            return None

    def add_events(self, events):
        """
        add events to g_cal calender
        :param g_cal: google calender object
        :param events: list of Events
        :return: list of the events
        """
        try:
            added = []
            for event in events:
                e = self.g_cal.events().insert(calendarId=self.CALENDER_ID,
                                               sendNotifications=False, body=event).execute()
                added.append(e)
                self.print_status(e, 'added')
            return added
        except Exception as err:
            print('Event was not created successfully')
            return None

    def print_status(self, e, operation):
        """
        Print the status of an event
        :param e: Event object
        :return:
        """
        print('''*** %r event %s:
	        Start: %s
	        End:   %s''' % (e['summary'].encode('utf-8'), operation,
                            e['start']['dateTime'], e['end']['dateTime']))

    def delete_events(self, events):
        deleted = []
        for event in events:
            deleted.append(self.g_cal.events().delete(calendarId=self.CALENDER_ID, eventId=event['id']).execute())
            self.print_status(event, 'deleted')
        return deleted

#
if __name__ == "__main__":
    # add scraped events

    g_cal = Calendar()
    events = scrape.get_events()
    num = scrape.save_events_to_db(events, 'events.db', 'new_events.db')
    added = g_cal.add_events(scrape.db_to_json('new_events.db'))
    del_events = g_cal.delete_events(added)

    # add example event

    # g_cal = Calendar()
    #     events = g_cal.add_events(EVENTS)
    #     del_events = g_cal.delete_events(events)

