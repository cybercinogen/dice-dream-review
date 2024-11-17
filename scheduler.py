# scheduler.py
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from scraper import scrape_reviews
from preprocessor import preprocess_reviews
from categorizer import categorize_reviews

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def scheduled_job():
    try:
        scrape_reviews()
        logging.info("Scraping completed.")
        preprocess_reviews()
        logging.info("Preprocessing completed.")
        categorize_reviews()
        logging.info("Categorization completed.")
    except Exception as e:
        logging.error(f"Error in scheduled job: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduled_job()  # Immediate first run
    scheduler.add_job(scheduled_job, 'interval', days=1)  # Run daily
    scheduler.start()
    logging.info("Scheduler started for daily runs.")

if __name__ == '__main__':
    start_scheduler()
