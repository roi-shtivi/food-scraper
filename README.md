# Dependencies
Install the following libraries:
```
pip install --upgrade requests bs4 google-api-python-client
```

# Running the script
```
python3 scraper.py
```

TODO: use parameters somehow

This library helps extracting events from various websites directly to your Google Calendar.

### Debug mode
At `calendar.py` you can chose the `CALENDAR_ID` to inject event into.
At `scraper.py` you can delete your newly added event using `g_cal.delete_events(added)`.
Both of this option is enable by default.



