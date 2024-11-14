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
    """Starts the scheduler to run `scheduled_job` every 3 minutes."""
    scheduler = BackgroundScheduler()
    # Set the job to run every 3 minutes for testing purposes
    scheduler.add_job(scheduled_job, 'interval', minutes=3)
    scheduler.start()
    logging.info("Scheduler started.")

if __name__ == '__main__':
    # Run individual function tests
    logging.info("Testing each function individually without the scheduler.")
    
    try:
        scrape_reviews()
        logging.info("Scrape test completed successfully.")
        
        preprocess_reviews()
        logging.info("Preprocess test completed successfully.")
        
        categorize_reviews()
        logging.info("Categorize test completed successfully.")
    except Exception as e:
        logging.error(f"Error during individual function tests: {e}")

    # Start the scheduler for interval-based execution
    start_scheduler()
    
    try:
        while True:
            time.sleep(2)  # Keeps the script running
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopped.")
