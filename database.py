import logging
from sqlalchemy import create_engine, Column, Integer, String, DateTime, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = 'sqlite:///reviews.db'
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define the Review model
class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column(String, unique=True, nullable=False)
    user_name = Column(String, nullable=True)
    rating = Column(Integer, nullable=True)
    content = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    category = Column(String, nullable=True)

# Create tables only if they don't exist
try:
    inspector = inspect(engine)
    if 'reviews' not in inspector.get_table_names():
        logger.info("Creating tables in the database...")
        Base.metadata.create_all(engine)
    else:
        logger.info("Tables already exist. Skipping table creation.")
except Exception as e:
    logger.error(f"Error during table creation or inspection: {e}")

def update_database_from_csv(csv_file='reviews.csv'):
    """
    Updates the database with reviews from the given CSV file.
    Ensures no duplicate records are added based on review_id.
    """
    session = Session()
    try:
        # Load CSV into DataFrame
        logger.info(f"Reading data from {csv_file}...")
        df = pd.read_csv(csv_file)

        # Process each row and add to the database if not already present
        new_reviews_count = 0
        for _, row in df.iterrows():
            if not session.query(Review).filter_by(review_id=row['review_id']).first():
                review = Review(
                    review_id=row['review_id'],
                    user_name=row.get('user_name', None),
                    rating=row.get('rating', None),
                    content=row.get('content', None),
                    date=row.get('date', None),
                    category=row.get('category', None)
                )
                session.add(review)
                new_reviews_count += 1

        # Commit the transaction
        session.commit()
        logger.info(f"Database updated with {new_reviews_count} new reviews.")
    except FileNotFoundError:
        logger.error(f"CSV file '{csv_file}' not found.")
    except KeyError as e:
        logger.error(f"Missing column in the CSV file: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while updating the database: {e}")
    finally:
        session.close()
