# scraper.py
import logging
import pandas as pd
from google_play_scraper import reviews, Sort
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def scrape_reviews(app_id='com.superplaystudios.dicedreams', days=7, max_reviews=500):
    """
    Scrapes Google Play reviews for the specified app.
    - app_id: App's package name.
    - days: Number of past days to scrape reviews.
    - max_reviews: Maximum number of reviews to fetch.
    """
    all_reviews = []
    today = datetime.now()
    start_date = today - timedelta(days=days)

    logging.info(f"Fetching reviews from {start_date.date()} to {today.date()}...")
    continuation_token = None
    fetched_count = 0
    retries = 0

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

            # Filter reviews by date
            for review in result:
                review_date = review['at']
                if review_date >= start_date:
                    all_reviews.append({
                        'review_id': review['reviewId'],
                        'user_name': review['userName'],
                        'rating': review['score'],
                        'content': review['content'],
                        'date': review_date.strftime('%Y-%m-%d'),
                        'category': 'Uncategorized'  # Default category
                    })
                    fetched_count += 1
                # Stop if we reach max_reviews
                if fetched_count >= max_reviews:
                    break

            # Stop if there's no continuation token
            if not continuation_token:
                break

        except Exception as e:
            retries += 1
            if retries > 3:
                logging.error("Maximum retries reached. Exiting scraper.")
                break
            logging.warning(f"Error occurred: {e}. Retrying in 5 seconds...")
            time.sleep(5)

    # Save reviews to CSV
    if all_reviews:
        df = pd.DataFrame(all_reviews)
        df.to_csv("reviews.csv", index=False)
        logging.info(f"Successfully fetched and saved {len(all_reviews)} reviews to reviews.csv.")
    else:
        logging.info("No reviews found in the specified date range.")

if __name__ == "__main__":
    scrape_reviews()
# scraper.py
import logging
import pandas as pd
from google_play_scraper import reviews, Sort
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def scrape_reviews(app_id='com.superplaystudios.dicedreams', days=7, max_reviews=500):
    """
    Scrapes Google Play reviews for the specified app.
    - app_id: App's package name.
    - days: Number of past days to scrape reviews.
    - max_reviews: Maximum number of reviews to fetch.
    """
    all_reviews = []
    today = datetime.now()
    start_date = today - timedelta(days=days)

    logging.info(f"Fetching reviews from {start_date.date()} to {today.date()}...")
    continuation_token = None
    fetched_count = 0
    retries = 0

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

            # Filter reviews by date
            for review in result:
                review_date = review['at']
                if review_date >= start_date:
                    all_reviews.append({
                        'review_id': review['reviewId'],
                        'user_name': review['userName'],
                        'rating': review['score'],
                        'content': review['content'],
                        'date': review_date.strftime('%Y-%m-%d'),
                        'category': 'Uncategorized'  # Default category
                    })
                    fetched_count += 1
                # Stop if we reach max_reviews
                if fetched_count >= max_reviews:
                    break

            # Stop if there's no continuation token
            if not continuation_token:
                break

        except Exception as e:
            retries += 1
            if retries > 3:
                logging.error("Maximum retries reached. Exiting scraper.")
                break
            logging.warning(f"Error occurred: {e}. Retrying in 5 seconds...")
            time.sleep(5)

    # Save reviews to CSV
    if all_reviews:
        df = pd.DataFrame(all_reviews)
        df.to_csv("reviews.csv", index=False)
        logging.info(f"Successfully fetched and saved {len(all_reviews)} reviews to reviews.csv.")
    else:
        logging.info("No reviews found in the specified date range.")

if __name__ == "__main__":
    scrape_reviews()
