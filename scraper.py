from calender import Calendar
import science_scrape
from db import Db

if __name__ == "__main__":
    """
    starting point for the scraper.
    """
    # add scraped events

    g_cal = Calendar()
    db = Db('events.db')
    events = science_scrape.get_events()
    new_events = db.remove_existing_events_from_list(events)
    added = g_cal.add_events([e.to_json() for e in new_events])
    db.save_events_to_db(new_events)
    del_events = g_cal.delete_events(added)  # debug-mode

    # TODO: use a parameter for this
    # add example event
    #
    # g_cal = Calendar()
    # events = g_cal.add_events(util.EXAMPLE_EVENTS)
    # del_events = g_cal.delete_events(events)
