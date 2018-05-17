from calender import Calendar
import science_scrape
import math_scrape
import db
import sys


if __name__ == "__main__":
    if len(sys.argv) > 3:
        cal_mark = sys.argv[1]
        debug = int(sys.argv[2])
        scrapers = sys.argv[3:]
        g_cal = Calendar(cal_mark)
        events = []
        if 'SCIENCE' in scrapers:
            events += science_scrape.get_events()
        if 'MATH' in scrapers:
            events += math_scrape.get_events()
        if not debug:
            num = db.save_events_to_db(events, 'events.db', 'new_events.db')
            added = g_cal.add_events(db.db_to_json('new_events.db'))
        else:
            num = db.save_events_to_db(events, 'debug_events.db',
                                       'debug_new_events.db')
            added = g_cal.add_events(db.db_to_json('debug_new_events.db'))
            del_events = g_cal.delete_events(added)
    else:
        raise AttributeError(
            "python3 scraper.py cal_mark debug SCRAPE_1 SCRAPER_2")
