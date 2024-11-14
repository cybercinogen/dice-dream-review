# scraper.py

import os
import warnings
import logging
import pandas as pd
from google_play_scraper import reviews, Sort
from datetime import datetime, timedelta


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Suppress warnings and logs for cleaner output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore")

def scrape_reviews(app_id='com.superplaystudios.dicedreams', days=7):
    all_reviews = []
    today = datetime.now()
    start_date = today - timedelta(days=days)

    logging.info("Starting to fetch reviews...")

    continuation_token = None
    while True:
        try:
            result, continuation_token = reviews(
                app_id,
                lang='en',
                country='us',
                sort=Sort.NEWEST,
                count=200,
                continuation_token=continuation_token
            )

            if not result:
                logging.info("No more reviews to fetch.")
                break

            stop_fetching = False

            for review in result:
                review_date = review['at']
                if review_date >= start_date:
                    all_reviews.append(review)
                else:
                    stop_fetching = True
                    break  # Stop the loop when reviews are older than start_date

            if stop_fetching or not continuation_token:
                break

        except Exception as e:
            logging.error(f"Error occurred while fetching reviews: {e}")
            break

    if all_reviews:
        df = pd.DataFrame(all_reviews)
        df.to_csv("reviews.csv", index=False)
        logging.info(f"{len(all_reviews)} reviews saved to reviews.csv.")
    else:
        logging.info("No new reviews to save.")

if __name__ == "__main__":
    scrape_reviews()
