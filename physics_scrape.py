from calender import Calendar

# Calendars id's
CALENDAR_ID_BIOPHYSICS = 'mail.huji.ac.il_6al194vs9273npoq6qt0kqoh7o@group.calendar.google.com'
CALENDAR_ID_CONDENSED_MATTER_SEMINAR = 'mail.huji.ac.il_suldq55m59ba8v8b4u9jer3b78@group.calendar.google.com'
CALENDAR_ID_HIGH_ENERGY_SEMINAR = 'mail.huji.ac.il_e1pfn2ackhvcrdt6im9lu1thog@group.calendar.google.com'
CALENDAR_ID_NANOPHOTONICS_OPTICS_SEMINAR = 'mail.huji.ac.il_1ldktmg3ndt3qm3lt8q591nhuk@group.calendar.google.com'
CALENDAR_ID_NONLINEAR_SEMINAR = 'mail.huji.ac.il_i88i469mrurc78b94p0tdgtjos@group.calendar.google.com'

# List of calendars id's
calendars_ids = [CALENDAR_ID_BIOPHYSICS, CALENDAR_ID_CONDENSED_MATTER_SEMINAR, CALENDAR_ID_HIGH_ENERGY_SEMINAR,
                 CALENDAR_ID_NANOPHOTONICS_OPTICS_SEMINAR, CALENDAR_ID_NONLINEAR_SEMINAR]

if __name__ == '__main__':
    events = []
    for cal_id in calendars_ids:
        service = Calendar(cal_id)
        events += service.to_events_objects()
