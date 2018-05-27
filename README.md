This library helps extracting events from various websites directly to your Google Calendar.

## Dependencies
### Python Libraries
Install the following libraries:
```
pip3 install --upgrade requests bs4 google-api-python-client
```
### Environment variables
- `'FFF_CAL_ID'` Calendar id to add (real) events to.
- `'TEST_CAL_ID'` Calendar id to add test events to.

Calendar id can be found on google calendar's settings.

## Running the script
Tested on `python3.6`.
```
python3 scraper.py <calendar> [-h] [--debug] [--all] [--scrapers SCRAPERS [SCRAPERS ...]]
```

- `calendar` parameter can take `FFF` or `TEST`.
### Examples
`python3 scraper.py FFF --all` will insert events to `FFF` calendar from all scrapers avialble
`python3 scraper.py TEST --scrapers SCIENCE MATH` will insert events to `TEST` calendar from `SCIENCE` and `MATH`
`python3 scraper.py FFF --d --all` will insert events to `TEST` calendar from all scrapers avialble and will delete them immediately.
