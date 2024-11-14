from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///reviews.db', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    review_id = Column(String, unique=True)
    user_name = Column(String)
    rating = Column(Integer)
    content = Column(String)
    date = Column(DateTime)
    category = Column(String)

Base.metadata.create_all(engine)

def save_reviews(reviews):
    session = Session()
    for rev in reviews:
        if not session.query(Review).filter_by(review_id=rev['reviewId']).first():
            review = Review(
                review_id=rev['reviewId'],
                user_name=rev['userName'],
                rating=rev['score'],
                content=rev['content'],
                date=rev['at'],
                category=rev['category']
            )
            session.add(review)
            print(f"Saved review with ID: {review.review_id}")
        else:
            print(f"Review with ID {rev['reviewId']} already exists. Skipping.")

    session.commit()
    session.close()
    print("All reviews have been committed to the database.")
