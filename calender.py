from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import os

SCOPES = 'https://www.googleapis.com/auth/calendar'  # read&write permissions


class Calendar:
    def __init__(self, cal_id):
        self.g_cal = setup()
        self.cal_id = cal_id

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
                e = self.g_cal.events().insert(calendarId=self.cal_id,
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
            End:   %s''' % (e['summary'], operation,
                            e['start']['dateTime'], e['end']['dateTime']))

    def delete_events(self, events):
        deleted = []
        for event in events:
            deleted.append(self.g_cal.events().delete(calendarId=self.cal_id, eventId=event['id']).execute())
            self.print_status(event, 'deleted')
        return deleted


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