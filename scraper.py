from calender import Calendar
import science_scrape
import db
import os

if __name__ == "__main__":
    """
    starting point for the scraper.
    """
    # add scraped events

    g_cal = Calendar()
    events = science_scrape.get_events()
    num = db.save_events_to_db(events, 'events.db', 'new_events.db')
    added = g_cal.add_events(db.db_to_json('new_events.db'))
    os.remove('new_events.db')
    # del_events = g_cal.delete_events(added)  # debug-mode

    # TODO: use a parameter for this
    # add example event
    #
    # g_cal = Calendar()
    # events = g_cal.add_events(util.EXAMPLE_EVENTS)
    # del_events = g_cal.delete_events(events)
