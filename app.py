# app.py

import os
from flask import Flask, render_template, request
from database import Session, Review
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    session = Session()
    categories = ["Bugs", "Complaints", "Crashes", "Praises", "Other"]
    dates = [(datetime.now() - timedelta(days=i)).date() for i in range(7)]

    selected_date = request.form.get('date')
    selected_category = request.form.get('category')

    reviews = []
    count = 0
    trend = []

    if selected_date and selected_category:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        # Fetch reviews for the selected date and category
        reviews = session.query(Review).filter(
            Review.date >= selected_date,
            Review.date < selected_date + timedelta(days=1),
            Review.category == selected_category
        ).all()
        count = len(reviews)

        # Calculate trend over the last 7 days
        for i in range(7):
            day = selected_date - timedelta(days=i)
            day_count = session.query(Review).filter(
                Review.date >= day,
                Review.date < day + timedelta(days=1),
                Review.category == selected_category
            ).count()
            trend.append({'date': day.strftime('%Y-%m-%d'), 'count': day_count})
        trend.reverse()

    session.close()
    return render_template('index.html', **locals())

if __name__ == "__main__":
    # Bind to Render's PORT environment variable or default to 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
