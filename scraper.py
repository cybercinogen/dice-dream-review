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

def scrape_reviews(app_id='com.superplaystudios.dicedreams', days=7, max_reviews=500):
    all_reviews = []
    today = datetime.now()
    start_date = today - timedelta(days=days)

    logging.info("Forcing fetch of reviews for the last 7 days...")

    continuation_token = None
    fetched_count = 0

    while fetched_count < max_reviews:
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

            # Collect reviews within the last 7 days
            for review in result:
                review_date = review['at']
                if review_date >= start_date:
                    all_reviews.append({
                        'review_id': review['reviewId'],
                        'user_name': review['userName'],
                        'rating': review['score'],
                        'content': review['content'],
                        'date': review['at'],
                        'category': 'Uncategorized'  # default until categorized
                    })
                    fetched_count += 1
                if fetched_count >= max_reviews:
                    break  # Stop once we've reached the max_reviews limit

            if fetched_count >= max_reviews or not continuation_token:
                break

        except Exception as e:
            logging.error(f"Error occurred while fetching reviews: {e}")
            break

    # Save reviews to CSV if any were fetched
    if all_reviews:
        df = pd.DataFrame(all_reviews)
        df.to_csv("reviews.csv", index=False)
        logging.info(f"Fetched and saved {len(all_reviews)} reviews to reviews.csv.")
    else:
        logging.info("No reviews found in the past 7 days.")

if __name__ == "__main__":
    scrape_reviews()
