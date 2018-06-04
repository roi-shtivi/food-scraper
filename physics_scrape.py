from calender import setup
from event import Event

# Calendars id's
CALENDAR_ID_BIOPHYSICS = 'mail.huji.ac.il_6al194vs9273npoq6qt0kqoh7o@group.calendar.google.com'
CALENDAR_ID_CONDENSED_MATTER_SEMINAR = 'mail.huji.ac.il_suldq55m59ba8v8b4u9jer3b78@group.calendar.google.com'
CALENDAR_ID_HIGH_ENERGY_SEMINAR = 'mail.huji.ac.il_e1pfn2ackhvcrdt6im9lu1thog@group.calendar.google.com'
CALENDAR_ID_NANOPHOTONICS_OPTICS_SEMINAR = 'mail.huji.ac.il_1ldktmg3ndt3qm3lt8q591nhuk@group.calendar.google.com'
CALENDAR_ID_NONLINEAR_SEMINAR = 'mail.huji.ac.il_i88i469mrurc78b94p0tdgtjos@group.calendar.google.com'

# List of calendars id's
calendars_ids = [CALENDAR_ID_BIOPHYSICS, CALENDAR_ID_CONDENSED_MATTER_SEMINAR, CALENDAR_ID_HIGH_ENERGY_SEMINAR,
                 CALENDAR_ID_NANOPHOTONICS_OPTICS_SEMINAR, CALENDAR_ID_NONLINEAR_SEMINAR]


def parse_event(event):
    """
    Parse from the response body of event details for new Event object
    :param event: google calendar event
    :return: new Event
    """
    event_inst = title = s_time = e_time = body = location = link = ""
    if 'organizer' in event and 'displayName' in event['organizer']:
        event_inst = event['organizer']['displayName']
    if 'summary' in event:
        title = event['summary']
    if 'start' in event and 'dateTime' in event['start']:
        s_time = event['start']['dateTime'].split('+')[0]
    if 'end' in event and 'dateTime' in event['end']:
        e_time = event['end']['dateTime'].split('+')[0]
    if 'description' in event:
        body = event['description']
    if 'location' in event:
        location = event['location']
    if 'htmlLink' in event:
        link = event['htmlLink']
    if location != "" and s_time != "" and title != "":
        return Event(event_inst, title, s_time, e_time, body, location, link)


def add_events(calendar_id):
    """
    Gets list of event from calendar_id and make from them Events objects list
    :param calendar_id: google calendar id
    :return: Events list
    """
    events_list = []
    page_token = None
    while True:
        events = service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
        for e in events['items']:
            event = parse_event(e)
            if event is not None:
                events_list.append(event)

        page_token = events.get('nextPageToken')
        if not page_token:
            break
    return events_list


def get_events():
    """
    Get's all events from every calendar_id and make one Event list
    :return: Events list
    """
    events = []
    for cal_id in calendars_ids:
        events += add_events(cal_id)
    return events


if __name__ == '__main__':
    service = setup()
    events = get_events()
    for e in events:
        print(e)
