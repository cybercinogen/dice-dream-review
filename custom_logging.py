import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler

# Define the logging setup function directly in this file
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()  # Logs to console
        ]
    )

# Set up logging
setup_logging()

# Importing the necessary functions from other modules
from scraper import scrape_reviews
from preprocessor import preprocess_reviews
from categorizer import categorize_reviews

def scheduled_job():
    try:
        scrape_reviews()
        preprocess_reviews()
        categorize_reviews()
        logging.info("Scheduled job completed successfully.")
    except Exception as e:
        logging.error(f"Error in scheduled job: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_job, 'cron', hour=1, minute=0)
    scheduler.start()
    logging.info("Scheduler started.")

if __name__ == '__main__':
    start_scheduler()
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopped.")
