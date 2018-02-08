# trackr

### What
An automated assistant that records my progress over time on sites I frequent and physical exercises I do.

### Why
Tracking my progress helps me create and keep up with long term goals. It helps the manager part of myself stay aware of the realities of the worker part of myself. This collection is intended to be a step toward automating that process and helping my manager make informed decisions.

### How
This script monitors my progress on some of the sites I use regularly. It runs a few times daily using cron and logs my progress on Duolingo.com, Chess.com, Codewars.com, Goodreads.com and HackerRank.com. Data is being kept and visualized in a .xlsx spreadsheet at the moment. Data is collected using a variety of methods, depending on the third party structure, including Beautiful Soup, Selenium and JSON data from APIs.

Physical exercises are not entirely automated. They require me to dictate my exercises to my phone the day they're performed. I dictate an email, via Siri, to a dedicated email account. The email is parsed and exercise counts are added to the appropriate cell based on the keywords in the email body and the date of the email.

Example email body: "daily limber one stretching 20" translates to the following commands:

Add 1 to that day's count of repetitions of my Daily Limber routine; Add 20 to that day's count of minutes spent intentional stretching
