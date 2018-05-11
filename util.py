EXAMPLE_EVENTS = [{
    'summary': 'Test',
    'description': 'Good food wow',
    "location": 'Danciger B',  # free form
    'start': {'dateTime': '2018-05-06T13:00:00',
              'timeZone': 'Asia/Jerusalem'},
    'end': {'dateTime': '2018-05-06T16:00:00',
            'timeZone': 'Asia/Jerusalem'},
}]


def to_google_format(date_time):
    try:
        return date_time.strftime('%Y-%m-%dT%H:%M:%S')
    except:
        return ''