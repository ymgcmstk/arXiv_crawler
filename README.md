# arXiv crawler
## What is this?
This is a system that crawls new papers uploaded on arXiv and sends emails to subscribers if there is any new paper.
This can be run on GoogleAppEngine(GAE).

## How to Use
First, you have to rewrite the following files.
- settings.py

`APP_NAME`: The name of this app. You don't have to rewrite if not needed.

`PAPER_LIMIT`: The maximum number of crawling times.

`SENDER_ADDRESS`: The email address that sends emails.

`TARGLIST`: The list of genres you want to crawl. Please write a genre name like 'cs.CV'.

`filter_user()`: The function to filter some users. You don't have to rewrite if not needed, but I recommend rewriting here in oreder to avoid being used by too much users and increasing the burden of your app.
- app.yaml

`application`: The name of your app.

Then, launch this app on GAE!