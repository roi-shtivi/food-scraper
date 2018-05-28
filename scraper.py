from calender import Calendar
import science_scrape
import db
import os
import argparse
import math_scrape

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


def get_cal_id(calendar_arg):
    if calendar_arg == 'FFF':
        return os.environ['FFF_CAL_ID']
    elif calendar_arg == 'TEST':
        return os.environ['TEST_CAL_ID']
    # Invalid calendar symbol
    else:
        raise ValueError("Invalid calendar id name")


def run(args, events, debug=False):
    cal_id = ''
    event_file = 'events.db'
    new_event_file = 'new_events.db'
    if debug:
        event_file = 'debug_events.db'
        new_event_file = 'debug_new_events.db'
        args.calendar = 'TEST'
    try:
        cal_id = get_cal_id(args.calendar)
    except ValueError:
        parser.error('Invalid calendar id name')
    except KeyError as e:
        parser.error('A match of the environment variable {0} was not found. You should define {0} at your local machine'
                     .format(e))
    g_cal = Calendar(cal_id)
    num = db.save_events_to_db(events, event_file, new_event_file)
    added = g_cal.add_events(db.db_to_json(new_event_file))
    if debug:
        g_cal.delete_events(added)
    os.remove(new_event_file)
    return added, num


if __name__ == "__main__":
    parser, args = parse_arguments()
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
        added, num = run(args, events)
    else:
        added, num = run(args, events, debug=True)
