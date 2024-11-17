# categorizer.py
import pandas as pd
import logging
from database import Session, Review
from transformers import pipeline
import re

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Load pre-trained classifier
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Refined keyword-based categorization
CATEGORY_KEYWORDS = {
    "Bugs": ["bug", "issue", "problem", "glitch", "error", "doesn't work", "not working"],
    "Complaints": ["complaint", "disappointed", "hate", "bad", "not happy", "annoyed", "ads"],
    "Crashes": ["crash", "freeze", "unresponsive", "stuck", "stops working", "closes", "hangs"],
    "Praises": ["love", "great", "awesome", "excellent", "best", "fantastic", "amazing"],
}

def match_keywords(content):
    """Categorize based on keywords with regex."""
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(re.search(rf"\b{keyword}\b", content, re.IGNORECASE) for keyword in keywords):
            return category
    return None

def categorize_reviews(batch_size=100):
    session = Session()
    try:
        df = pd.read_csv('preprocessed_reviews.csv')
        if df.empty:
            logging.info("No reviews to categorize.")
            return
        
        for start in range(0, len(df), batch_size):
            batch = df.iloc[start:start + batch_size]
            for _, row in batch.iterrows():
                content = row['content']
                category = match_keywords(content)

                if not category:
                    prediction = classifier(content)[0]
                    label = prediction['label']
                    if label == "POSITIVE":
                        category = "Praises"
                    else:
                        if any(re.search(rf"\b{kw}\b", content.lower()) for kw in CATEGORY_KEYWORDS["Bugs"]):
                            category = "Bugs"
                        elif any(re.search(rf"\b{kw}\b", content.lower()) for kw in CATEGORY_KEYWORDS["Complaints"]):
                            category = "Complaints"
                        elif any(re.search(rf"\b{kw}\b", content.lower()) for kw in CATEGORY_KEYWORDS["Crashes"]):
                            category = "Crashes"
                        else:
                            category = "Other"
                
                review = Review(
                    review_id=row['review_id'],
                    user_name=row['user_name'],
                    rating=row['rating'],
                    content=content,
                    date=pd.to_datetime(row['date']),
                    category=category
                )
                session.add(review)
                logging.info(f"Categorized review {row['review_id']} as {category}")

        session.commit()
        logging.info("Batch categorization complete.")
    except Exception as e:
        logging.error(f"Error during categorization: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    categorize_reviews()
