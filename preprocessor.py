# preprocessor.py

import pandas as pd
import re
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text

def preprocess_reviews():
    try:
        df = pd.read_csv("reviews.csv")
        df['content'] = df['content'].apply(preprocess_text)
        df.to_csv("preprocessed_reviews.csv", index=False)
        logging.info("Preprocessed reviews saved to preprocessed_reviews.csv.")
    except FileNotFoundError as e:
        logging.error("reviews.csv file not found. Make sure scraper has run.")
    except Exception as e:
        logging.error(f"Error during preprocessing: {e}")

if __name__ == "__main__":
    preprocess_reviews()
