# vodovod-notifier

## Overview

**BVK Planned Water Outage Notifier** is a script that monitors website of Belgrade Waterworks and Sewerage (BVK) for updates about planned maintenance and water supply interruptions. Users can subscribe to receive email notifications for municipalities that he requests, written in *Serbian Cyrillic*. The script checks for changes every 24 hours, ensuring timely alerts about any new or updated information.

## Features

-  **Web Scraping**: Uses `requests` and `BeautifulSoup` to scrape and parse the BVK planned works page.
-  **Email Notifications**: Sends HTML-formatted email alerts, using SMTPlib and email.mime Python libraries, when new relevant updates are detected.
-  **Automated Checks**: Runs an infinite loop to check for changes every 24 hours.
-  **Change Detection**: Compares old and new notifications to detect and send only new updates.

## How It Works

1. The script scrapes the BVK page and extracts notification paragraphs.
2. The user inputs a list of municipalities (in Cyrillic).
3. The user inputs his email to which he wants to receive notifications.
4. It filters updates by municipality and matches them with user input.
5. Relevant updates are emailed to the user.
6. Every 24 hours, the script repeats the process and sends notifications if new data is found.

## Disclaimer

This script is not affiliated with or endorsed by BVK. It simply automates publicly available information for user convenience.
