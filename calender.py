from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from event import Event
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
                e = self.g_cal.events().insert(
                            calendarId=self.cal_id,
                            sendNotifications=False,
                            body=event
                        ).execute()
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
        """
        Deletes a list of events
        :param e: Events object
        :return: a list of deleted events
        """
        deleted = []
        for event in events:
            deleted.append(self.g_cal.events().delete(
                calendarId=self.cal_id,
                eventId=event['id']
                ).execute())
            self.print_status(event, 'deleted')
        return deleted

    def get_events(self):
        """
        Gets all the event from calendar
        :return: google calendar events list
        """
        events_list = []
        page_token = None
        while True:
            events = self.g_cal.events().list(calendarId=self.cal_id, pageToken=page_token).execute()
            for e in events['items']:
                events_list.append(e)
            page_token = events.get('nextPageToken')
            if not page_token:
                break

        return events_list

    def to_events_objects(self):
        """
        Convert all the event in the calendar to Event objects list
        :return: Events list
        """
        google_events = self.get_events()
        events_list = []
        for i in range(len(google_events)):
            event = self.parse_event(google_events[i], i)
            if event is not None:
                events_list.append(event)

        return events_list

    def parse_event(self, event, i):
        """
        Parse from the response body of event details for new Event object
        :param event: google calendar event
        :param i: number of event in the google calendar
        :return: new Event
        """
        event_inst = title = s_time = e_time = body = location = link = ""
        try:
            s_time = event['start']['dateTime'].split('+')[0]
            location = event['location']
            title = event['summary']
        except:
            print("Error: Missing start time/location/title. event number: {} from calendar id: {}".
                  format(i, self.cal_id))

        if 'organizer' in event and 'displayName' in event['organizer']:
            event_inst = event['organizer']['displayName']
        if 'end' in event and 'dateTime' in event['end']:
            e_time = event['end']['dateTime'].split('+')[0]
        if 'description' in event:
            body = event['description']
        if 'htmlLink' in event:
            link = event['htmlLink']
        if location != "" and s_time != "" and title != "":
            return Event(event_inst, title, s_time, e_time, body, location, link)


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
    except Exception as err:
        print('google calendar object was not initialize successfully')
        raise err
