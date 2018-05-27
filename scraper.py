from calender import Calendar
import science_scrape
import math_scrape
import db
import os
import argparse

SCRAPERS = [math_scrape, science_scrape]
SCRAPERS_NAMES = [x.__name__ for x in SCRAPERS]

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('calendar',
                        help="calendar symbolic name where events will be added into. currently supporting: " +
                             ("\'{}\' " * len(SCRAPERS)).format(*SCRAPERS_NAMES))
    parser.add_argument('--debug', '--d', '-debug', '-d',
                        help="debug mode, events will be added to TEST calendar and will be immediately deleted",
                        action='store_true')
    parser.add_argument('--all', '-all', help="activate all scrapers",
                        action='store_true')
    parser.add_argument('--scrapers', '--l', '-scrapers', '-l', nargs='+',
                        help="list of scrapers that will be used")
    return parser, parser.parse_args()


def get_cal_id():
    if args.calendar == 'FFF':
        return os.environ['FFF_CAL_ID']
    elif args.calendar == 'TEST':
        return os.environ['TEST_CAL_ID']
    # Invalid calendar symbol
    else:
        raise ValueError("Invalid calendar id name")


if __name__ == "__main__":
    parser, args = parse_arguments()
    cal_id = ''
    try:
        cal_id = get_cal_id()
    except ValueError:
        parser.error('Invalid calendar id name')
    # no -all flag or scrapers list was accepted
    if not (args.all or args.scrapers):
        parser.error('No action requested, add --all or --scrapers SCRAPERS [SCRAPERS ...]')
    # both -all and scrapers list was accepted
    if args.all and args.scrapers:
        parser.error('Too many actions requested, --all and --scrapers is ambiguous')
    if args.all:
        args.scrapers = SCRAPERS_NAMES
    events = []
    for scraper in SCRAPERS:
        if scraper.__name__ in args.scrapers:
            events += scraper.get_events()
    if not args.debug:
        g_cal = Calendar(cal_id)
        num = db.save_events_to_db(events, 'events.db', 'new_events.db')
        added = g_cal.add_events(db.db_to_json('new_events.db'))
        os.remove('new_events.db')
    else:
        g_cal = Calendar(os.environ['TEST_CAL_ID'])
        num = db.save_events_to_db(events, 'debug_events.db', 'debug_new_events.db')
        added = g_cal.add_events(db.db_to_json('debug_new_events.db'))
        del_events = g_cal.delete_events(added)
        os.remove('debug_new_events.db')
