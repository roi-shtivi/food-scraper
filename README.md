This library helps extracting events from various websites directly to your Google Calendar.

### Dependencies
Install the following libraries:
```
pip install --upgrade requests bs4 google-api-python-client
```

#### Running the script
```
python3 scraper.py CAL_MARKER DEBUG SCRAPER_1 SCRAPE_2
```
* `CAL_MARKER` represent the calendar events will be added into.
Can be `FFF` or `TEST`.
* `DEBUG` represent a mode where the events will be immediately deleted after
they were added, also the events will be added to a new .db files.
Can be `0` or `1`.
* `SCRAPE_i` represent the name of the scrape that will be used.
Currently can be `SCIENCE` or `MATH`.
