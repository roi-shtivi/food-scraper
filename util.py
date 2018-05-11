def to_google_format(date_time):
    try:
        return date_time.strftime('%Y-%m-%dT%H:%M:%S')
    except:
        return ''