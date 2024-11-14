import pandas as pd
import logging
from database import Session, Review
from transformers import pipeline
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Load the on-device LLM classifier
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Define category keywords
CATEGORY_KEYWORDS = {
    "Bugs": ["bug", "issue", "problem", "glitch", "error"],
    "Complaints": ["complaint", "not working", "disappointed", "hate", "bad"],
    "Crashes": ["crash", "freeze", "unresponsive", "stuck"],
    "Praises": ["love", "great", "awesome", "excellent", "best", "fantastic"],
    "Other": []  # No keywords, fallback category
}

def match_keywords(content):
    """Categorize based on keywords."""
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(re.search(rf"\b{keyword}\b", content, re.IGNORECASE) for keyword in keywords):
            return category
    return None

def categorize_reviews():
    try:
        # Load preprocessed_reviews.csv
        df = pd.read_csv('preprocessed_reviews.csv')
        
        if 'date' not in df.columns:
            logging.error("The 'date' column is missing in preprocessed_reviews.csv.")
            return
        
        # Initialize database session
        session = Session()

        # Loop through each review and categorize it
        for _, row in df.iterrows():
            # Check for keyword-based category
            category = match_keywords(row['content'])
            
            # If no keyword match, use LLM for categorization
            if not category:
                prediction = classifier(row['content'])[0]
                label = prediction['label']
                if label == "POSITIVE":
                    category = "Praises"
                elif label == "NEGATIVE":
                    # Choose between Bugs, Complaints, Crashes, or Other
                    category = "Complaints"  # Default fallback for negative reviews
                    
            # Final fallback category
            if not category:
                category = "Other"
            
            # Add categorized review to the database
            review = Review(
                review_id=row['review_id'],
                user_name=row['user_name'],
                rating=row['rating'],
                content=row['content'],
                date=pd.to_datetime(row['date']),
                category=category
            )
            session.add(review)
            logging.info(f"Categorized review {row['review_id']} as {category}")

        # Commit all changes to the database
        session.commit()
        logging.info("All reviews categorized and saved to the database.")
    
    except Exception as e:
        logging.error(f"Error during categorization: {e}")
    
    finally:
        session.close()

if __name__ == "__main__":
    categorize_reviews()
