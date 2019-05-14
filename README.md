# trackr

### Why
I like to track my progress with long term goals, I think it helps me stay focused. Or rather, I think it would help me stay focused if I kept it up long term. It would help the manager part of myself stay aware of the realities of the worker part of myself. 

But if I don't get reminded eventually I get distracted and forget. So I make a reminder but generic reminders lose their effect pretty quick and I stop seeing them. What gets my attention is personalized, responsive visuals that show my progress. 

Realistically, I'm never going to keep up with manually documenting progress though, so it needs to be automated.

### What
That's why I'm building this automated assistant that records my activity toward my long term goals and presents me with visuals of my progress. Plus, one of those goals is improving my programming, so it's already time well spent!

### How

##### Digital activity - entirely automated
This script monitors my progress on some of the sites I use regularly. It runs a few times daily using cron and logs my progress on Duolingo.com, Chess.com, Codewars.com and Goodreads.com. Data is collected using a variety of methods, depending on the third party structure, including Beautiful Soup, Selenium and JSON data from APIs. Data is stored in an SQLite database.

##### Analog activity - largely automated
Physical exercises and time spent in deep focus are not entirely automated. They require me to dictate my activity to my phone the day it's performed. I dictate an email, via Siri, to a dedicated email account. The email is parsed and activity counts are added to the appropriate cell based on the keywords in the email body and the date of the email.

Example email subject: "Body"
Example email body: "daily limber one stretching 20" 
Translates to the following commands: Add 1 to that day's count of repetitions of my Daily Limber routine. Add 20 to that day's count of minutes spent intentional stretching.

##### Visuals
On predetermined intervals, currently Sundays and every 4th Sunday, figures are launched from the background cronjob. They show my weekly activity and "monthly" activity respectively (in reality, it's 28 days for consistency), along with overlaying plots that show how I'm doing relative to my goals.


### Upcoming

I built a dirty, functional version and let it sit for a while. Now I'm cleaning it up with a bunch of knowledge I've gained since then and fixing some bugs that showed themselves over time. 

Soon I'll write an Anki module, since that's become my primary language practice tool as well as a supplementary programming tool. Then I may look into writing a GitHub module based on commit history.
