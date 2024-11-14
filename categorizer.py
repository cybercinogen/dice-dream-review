import pandas as pd
import logging
from database import Session, Review
from transformers import pipeline
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Load the on-device LLM classifier
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Define refined category keywords with stricter criteria for matching
CATEGORY_KEYWORDS = {
    "Bugs": ["bug", "issue", "problem", "glitch", "error", "doesn't work", "not working"],
    "Complaints": ["complaint", "disappointed", "hate", "bad", "not happy", "annoyed", "too many ads"],
    "Crashes": ["crash", "freeze", "unresponsive", "stuck", "stops working", "closes", "hangs"],
    "Praises": ["love", "great", "awesome", "excellent", "best", "fantastic", "amazing", "enjoy"],
    "Other": []  # No keywords, acts as a fallback category
}

def match_keywords(content):
    """Categorize based on keywords with a stricter regex match."""
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
            content = row['content']
            # Check for keyword-based category
            category = match_keywords(content)
            
            # If no keyword match, use LLM for categorization
            if not category:
                prediction = classifier(content)[0]
                label = prediction['label']
                if label == "POSITIVE":
                    category = "Praises"
                elif label == "NEGATIVE":
                    # Distinguish between Complaints and Bugs based on keyword match
                    if any(word in content.lower() for word in CATEGORY_KEYWORDS["Bugs"]):
                        category = "Bugs"
                    elif any(word in content.lower() for word in CATEGORY_KEYWORDS["Complaints"]):
                        category = "Complaints"
                    elif any(word in content.lower() for word in CATEGORY_KEYWORDS["Crashes"]):
                        category = "Crashes"
                    else:
                        category = "Other"  # If none match, fallback to "Other"
            
            # Final fallback category for unclassified reviews
            if not category:
                category = "Other"
            
            # Add categorized review to the database
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

        # Commit all changes to the database
        session.commit()
        logging.info("All reviews categorized and saved to the database.")
    
    except Exception as e:
        logging.error(f"Error during categorization: {e}")
    
    finally:
        session.close()

if __name__ == "__main__":
    categorize_reviews()
