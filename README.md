This library helps extracting events from various websites directly to your Google Calendar.

### Dependencies
Install the following libraries:
```
pip install --upgrade requests bs4 google-api-python-client
```
Environment variables `'FFF_CAL_ID'` and `'TEST_CAL_ID'` should be set with the corresponding calendar's ids.

#### Running the script
```
usage: scraper.py calendar [-h] [--debug] [--all] [--scrapers SCRAPERS [SCRAPERS ...]]
```
For example:
`FFF --all` will insert events to `FFF` calendar from all scrapers avialble
`TEST --scrapers SCIENCE MATH` will insert events to `TEST` calendar from `SCIENCE` and `MATH`
`FFF -d --all` will insert events to `TEST` calendar from all scrapers avialble and will delete them immidiatly
