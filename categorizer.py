# categorizer.py

import os
import warnings
import logging
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from scipy.special import softmax
from database import save_reviews

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Suppress warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore")

# Model setup
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Category Keywords
category_keywords = {
    "Bugs": ["bug", "issue", "error", "problem", "glitch", "fix"],
    "Complaints": ["hate", "dislike", "bad", "terrible", "annoying", "poor"],
    "Crashes": ["crash", "freeze", "unresponsive", "hang", "close unexpectedly"],
    "Praises": ["love", "amazing", "great", "excellent", "awesome", "perfect", "good", "impressive", "satisfied"],
    "Other": []
}

def classify_review(text):
    try:
        inputs = tokenizer(text, return_tensors="pt")
        outputs = model(**inputs)
        scores = softmax(outputs[0][0].detach().numpy())

        if scores[2] > 0.5:
            category = "Praises"
        elif scores[0] > 0.6:
            category = "Complaints"
        else:
            category = "Other"

        for key, keywords in category_keywords.items():
            if any(keyword.lower() in text.lower() for keyword in keywords):
                category = key
                break

        return category
    except Exception as e:
        logging.error(f"Error in classification: {e}")
        return "Other"

def categorize_reviews():
    try:
        df = pd.read_csv("preprocessed_reviews.csv")
        df['category'] = df['content'].apply(classify_review)
        reviews_list = df.to_dict(orient='records')
        save_reviews(reviews_list)
        logging.info("Categorized reviews saved to the database.")
    except FileNotFoundError as e:
        logging.error("preprocessed_reviews.csv not found. Make sure preprocessing has run.")
    except Exception as e:
        logging.error(f"Error during categorization: {e}")

if __name__ == "__main__":
    categorize_reviews()
