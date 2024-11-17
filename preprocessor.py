import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def preprocess_reviews():
    try:
        # Load reviews.csv and check for required columns
        df = pd.read_csv('reviews.csv')
        required_columns = ['review_id', 'user_name', 'rating', 'content', 'date', 'category']
        
        # Check if all required columns are present
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            logging.error(f"Missing columns in reviews.csv: {missing_columns}")
            return
        
        # Preprocess if columns are present
        # Additional preprocessing steps here if required
        
        df.to_csv('preprocessed_reviews.csv', index=False)
        logging.info("Preprocessed reviews saved to preprocessed_reviews.csv.")

    except Exception as e:
        logging.error(f"Error during preprocessing: {e}")

if __name__ == "__main__":
    preprocess_reviews()
