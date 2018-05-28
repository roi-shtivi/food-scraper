from calender import Calendar
import science_scrape
import db
import os
import argparse

SCRAPERS = [science_scrape]
SCRAPERS_NAMES = [x.__name__ for x in SCRAPERS]

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('calendar',
                        help="Calendar symbolic name where events will be added into. \
                        Currently supporting: FFF, TEST")
    parser.add_argument('--debug', '--d', '-debug', '-d',
                        help="debug mode, events will be added to TEST calendar and will be immediately deleted",
                        action='store_true')
    parser.add_argument('--all', '-all', help="activate all scrapers",
                        action='store_true')
    parser.add_argument('--scrapers', '--l', '-scrapers', '-l', nargs='+',
            help="List of scrapers that will be used. Currently supporting:" +
                             (" \'{}\'" * len(SCRAPERS)).format(*SCRAPERS_NAMES))
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
        parser.error('Invalid calendar name')
    except KeyError as e:
        parser.error('Environment variable {0} was not found. You should define {0} in your local machine.'
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
        parser.error('No scrapers selected, use --all or --scrapers <SCRAPER1 SCRAPER2 ...>')
    # both -all and scrapers list was accepted
    if args.all and args.scrapers:
        parser.error('--all and --scrapers is ambiguous. Use only one of them.')
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
