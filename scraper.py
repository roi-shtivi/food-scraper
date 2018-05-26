from calender import Calendar
import science_scrape
import math_scrape
import db
import os
import argparse

SCRAPERS = ['SCIENCE', 'MATH']
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('calendar', help="calendar symbolic name where events will be added into.")
    parser.add_argument('--debug', '--d', '-debug', '-d',
                        help="debug mode, events will be added to TEST calendat and will be immidatly deleted",
                        action='store_true')
    parser.add_argument('--all', '-all', help="activate all scrapers", action='store_true')
    parser.add_argument('--scrapers', '--l', '-scrapers', '-l', nargs='+', help="list of scrapers that will be used")
    args = parser.parse_args()
    if not (args.all or args.scrapers):
        parser.error('No action requested, add --all or --scrapers SCRAPERS [SCRAPERS ...]')
    if args.all and args.scrapers:
        parser.error('Too many actions requested, --all and --scrapers is ambiguous')
    if args.all:
        args.scrapers = SCRAPERS
    events = []
    if 'SCIENCE' in args.scrapers:
        events += science_scrape.get_events()
    if 'MATH' in args.scrapers:
        events += math_scrape.get_events()
    if not args.debug:
        g_cal = Calendar(args.calendar)
        num = db.save_events_to_db(events, 'events.db', 'new_events.db')
        added = g_cal.add_events(db.db_to_json('new_events.db'))
        os.remove('new_events.db')
    else:
        g_cal = Calendar('TEST')
        num = db.save_events_to_db(events, 'debug_events.db', 'debug_new_events.db')
        added = g_cal.add_events(db.db_to_json('debug_new_events.db'))
        del_events = g_cal.delete_events(added)
        os.remove('debug_new_events.db')
