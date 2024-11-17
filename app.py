import os
from flask import Flask, render_template, request
from database import Session, Review
from datetime import datetime, timedelta
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/test_db')
def test_db():
    session = Session()
    try:
        # Test query to check if the connection is successful
        result = session.query(Review).first()
        if result:
            return f"Connection successful, first review ID: {result.review_id}"
        else:
            return "Connection successful, but no reviews found"
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        return "Database connection failed"
    finally:
        session.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    session = Session()

    # Define categories and last 7 days for date selection
    categories = ["Bugs", "Complaints", "Crashes", "Praises", "Other"]
    dates = [(datetime.now() - timedelta(days=i)).date() for i in range(7)]

    # Retrieve selected category and date from form
    selected_date = request.form.get('date', None)
    selected_category = request.form.get('category', None)

    # Initialize variables to store reviews, count, and trend
    reviews = []
    count = 0
    trend = []

    try:
        logging.info(f"Selected date: {selected_date}, Selected category: {selected_category}")

        # If date and category are selected, fetch reviews
        if selected_date and selected_category:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            
            # Query for selected date and category
            reviews = session.query(Review).filter(
                Review.date >= selected_date,
                Review.date < selected_date + timedelta(days=1),
                Review.category == selected_category
            ).all()
            count = len(reviews)
            logging.info(f"Fetched {count} reviews for {selected_date} in category {selected_category}")

            # Calculate trend over the last 7 days for the selected category
            for i in range(7):
                day = selected_date - timedelta(days=i)
                day_count = session.query(Review).filter(
                    Review.date >= day,
                    Review.date < day + timedelta(days=1),
                    Review.category == selected_category
                ).count()
                trend.append({'date': day.strftime('%Y-%m-%d'), 'count': day_count})
            trend.reverse()

    except Exception as e:
        logging.error(f"Error fetching reviews: {e}")

    finally:
        session.close()

    return render_template(
        'index.html',
        categories=categories,
        dates=dates,
        selected_date=selected_date,
        selected_category=selected_category,
        reviews=reviews,
        count=count,
        trend=trend
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
