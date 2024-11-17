# scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from scraper import scrape_reviews
import time

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule scrape_reviews to run once a day at 1 AM
    scheduler.add_job(scrape_reviews, 'cron', hour=1, minute=0)
    scheduler.start()
    print("Scheduler started.")

if __name__ == '__main__':
    start_scheduler()
    # Keep the script running
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        pass
