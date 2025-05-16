# vodovod-notifier

## Overview

**BVK Planned Water Outage Notifier** is a script that monitors the website of Belgrade Waterworks and Sewerage (BVK) for updates about planned maintenance and water supply interruptions. Users receive email notifications for municipalities, streets and neighborhoods that they request, written in *Serbian Cyrillic*. The script checks for changes every 24 hours, ensuring timely alerts about any new or updated information.

## Features

-  **Web Scraping**: Uses `requests` and `BeautifulSoup` to scrape and parse the BVK planned works page.
-  **Email Notifications**: Sends HTML-formatted email alerts, using smtplib and email.mime Python libraries, when new relevant updates are detected.
-  **Automated Checks**: Automatically checks for updates **every 24 hours** using `APScheduler`
-  **Change Detection**: Compares old and new notifications to detect and send only new updates.
-  **User-Specific Filtering**: Sends alerts **only** for user-selected streets and neighborhoods in municipalities that interest them. 

## How It Works

1. The script scrapes the BVK page and extracts notification paragraphs.
2. Users provide (all written in *Serbian Cyrillic*)
     - A list of municipalities
     - A list of streets and neighborhoods for each selected municipality
     - Their email address to which they want to receive notifications
3. It filters updates by municipality, streets and neighborhoods and matches them with user input.
4. Relevant updates are emailed to the user.
5. Every 24 hours, the script repeats the process and sends notifications if new data is found.

## Required Libraries

- `requests`
- `beautifulsoup4`
- `apscheduler`

```bash
pip install requests beautifulsoup4 apscheduler
```

## Disclaimer

This script is not affiliated with or endorsed by BVK. It simply automates publicly available information for user convenience.
