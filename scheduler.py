import sys
import os
import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler

# Define the logging setup function to log to both console and file
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),  # Logs to the console (terminal)
            logging.FileHandler("scheduler.log")  # Logs to a file
        ]
    )

# Set up logging
setup_logging()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)  # Enable APScheduler debugging

# Importing the necessary functions from other modules
from scraper import scrape_reviews
from preprocessor import preprocess_reviews
from categorizer import categorize_reviews

def scheduled_job():
    """Runs the entire scraping, preprocessing, and categorizing job."""
    try:
        logging.info("Starting scheduled job...")
        
        # Run each function and log progress
        scrape_reviews()
        logging.info("Completed scraping reviews.")
        
        preprocess_reviews()
        logging.info("Completed preprocessing reviews.")
        
        categorize_reviews()
        logging.info("Completed categorizing reviews.")
        
        logging.info("Scheduled job completed successfully.")
    except Exception as e:
        logging.error(f"Error in scheduled job: {e}")

def start_scheduler():
    """Starts the scheduler to run `scheduled_job` every 24 hours after the first run."""
    scheduler = BackgroundScheduler()
    
    # Run the job immediately for the first time
    logging.info("Running the job immediately for the first execution.")
    scheduled_job()
    
    # Schedule the job to run every 24 hours after the first run
    scheduler.add_job(scheduled_job, 'interval', days=1)
    scheduler.start()
    logging.info("Scheduler started, next runs will occur every 24 hours.")

if __name__ == '__main__':
    # Start the scheduler
    start_scheduler()
    
    try:
        while True:
            time.sleep(2)  # Keeps the script running
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopped.")
