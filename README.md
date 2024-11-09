
# **Dice Dreams Review Scraper and Categorizer**

This project is a fully containerized application designed to scrape, preprocess, categorize, and store Google Play Store reviews for the game *Dice Dreams*. The application includes an API with a scheduler that scrapes new reviews daily, categorizes them, and saves them to a database for efficient retrieval.

## **Project Structure**

```plaintext
dice_dreams_reviews/
├── app.py               # Flask API for serving categorized reviews
├── scheduler.py         # Scheduler for automating the daily scraping and categorization
├── scraper.py           # Scrapes Google Play Store reviews and saves to CSV
├── preprocessor.py      # Preprocesses raw review data
├── categorizer.py       # Categorizes reviews based on defined labels
├── database.py          # Database setup and review-saving logic
├── custom_log_config.py # Logging configuration (if needed by scripts)
├── Dockerfile           # Docker configuration for containerizing the app
├── requirements.txt     # List of dependencies for the project
├── README.md            # Project documentation
└── start.sh             # Script to run both scheduler and API in Docker
```

## **Project Overview**

This application automates the entire process of review scraping, categorization, and retrieval through a REST API. Here’s a quick summary of the main functionality:

1. **Scraping**: `scraper.py` uses `google-play-scraper` to pull reviews from *Dice Dreams* and saves them to a CSV file for processing.
2. **Preprocessing**: `preprocessor.py` preprocesses the scraped data, performing tasks like text normalization and punctuation removal.
3. **Categorization**: `categorizer.py` uses a pre-trained NLP model and keyword-based logic to categorize reviews into five categories: *Bugs*, *Complaints*, *Crashes*, *Praises*, and *Other*.
4. **Scheduler**: `scheduler.py` uses `APScheduler` to run the full scraping, preprocessing, and categorization workflow daily.
5. **API**: `app.py` provides an API to search and retrieve categorized reviews, enabling quick access to relevant feedback.

## **Design Choices and Justifications**

### **1. Model Selection for Categorization**
   - We use a pre-trained NLP model for sentiment analysis combined with keyword-based filtering for enhanced accuracy. This approach ensures good performance while keeping the model size and computational load manageable.

### **2. Containerization with Docker**
   - Containerizing the application ensures consistency across development, testing, and deployment environments. It also meets the assignment requirement for deployability, making the app portable and easier to run on different platforms.

### **3. Scheduled Automation**
   - `scheduler.py` runs the scraper daily using `APScheduler`, meeting the requirement for ongoing data collection without manual intervention.

### **4. Logging Configuration**
   - Each module (e.g., `scraper.py`, `preprocessor.py`, `categorizer.py`) has independent logging to avoid circular import issues. The `logging.basicConfig` function ensures consistent log formatting across scripts for easier debugging.

## **Setup and Installation**

### **Prerequisites**

- **Docker**: Ensure Docker is installed and running on your system.
- **Python 3.8+**: Required for local development and testing.

### **Clone the Repository**

```bash
git clone https://github.com/cybercinogen/dice_dreams_reviews.git
cd dice_dreams_reviews
```

### **Environment Variables**

- No specific environment variables are needed for local development. However, database and application environment variables might be required if deployed on a cloud server.

### **Installing Dependencies**

1. **Install dependencies (for local development only)**:

    ```bash
    pip install -r requirements.txt
    ```

2. **Run the application locally** (for testing):

    ```bash
    python scheduler.py   # Starts the scraping and categorization workflow
    python app.py         # Starts the Flask API
    ```

### **Building and Running the Docker Container**

1. **Build the Docker image**:

    ```bash
    docker build -t dice-dreams-app .
    ```

2. **Run the Docker container**:

    ```bash
    docker run -d -p 5000:5000 --name dice-dreams-container dice-dreams-app
    ```

3. **Access the API**:

   The API will be accessible at `http://localhost:5000`.

### **Automated Daily Scraping with Scheduler**

`APScheduler` in `scheduler.py` schedules the job to scrape, preprocess, and categorize reviews daily. The scheduler can be adjusted in `scheduler.py` by modifying the `cron` parameters.

## **API Documentation**

The API serves as an interface to access the categorized reviews and includes the following endpoints:

1. **Retrieve Categorized Reviews**

   - **URL**: `/`
   - **Method**: `GET`
   - **Parameters**: 
     - `date`: Date of reviews to retrieve (optional).
     - `category`: Review category (e.g., *Bugs*, *Praises*).

2. **Example Request**:

   ```bash
   curl -X GET "http://localhost:5000/?date=2024-11-05&category=Praises"
   ```

3. **Response**:
   
   ```json
   {
     "reviews": [
       {
         "user_name": "John Doe",
         "rating": 5,
         "content": "Love this game, very addictive!",
         "date": "2024-11-05",
         "category": "Praises"
       },
       ...
     ]
   }
   ```

## **Logging and Error Handling**

Each module has independent logging to capture key events and errors:

- **Logging**: Configured using `logging.basicConfig` in each script. Logs provide timestamps and severity levels for easier debugging.
- **Error Handling**: `try-except` blocks are used around key functions (e.g., `scrape_reviews` in `scraper.py`) to catch and log errors, ensuring the workflow continues without interruptions.

## **Design Challenges and Solutions**

1. **Circular Import Issues**:
   - Moving logging configuration to each script individually resolved circular import issues, improving modularity.
  
2. **Data Processing Consistency**:
   - The use of CSV files in the data pipeline allows easy inspection and debugging of intermediate steps (e.g., raw, preprocessed, categorized reviews).

## **Deployment Guide**

1. **Deploy on Cloud**: For deploying on cloud services like AWS, GCP, or Azure, use the Docker image. Ensure environment variables for database configuration (if using cloud databases) are appropriately set.
2. **Set Up Daily Job on Server**: Use `cron` (Linux) or scheduled tasks (Windows) to run `docker exec` commands that call `scheduler.py` daily if not using `APScheduler` in production.

Example `cron` job:
```bash
0 1 * * * docker exec dice-dreams-container python scheduler.py
```

## **Best Practices for Scalability**

- **Batch Processing**: Future improvements could include processing reviews in batches to handle larger volumes of data.
- **Logging Levels**: For production, set logging levels to `WARNING` or `ERROR` to avoid excessive logging.
- **API Rate Limiting**: Implement rate limiting on the API for scalable public access.

## **Contributing**

Feel free to fork this repository and submit pull requests for additional functionality or bug fixes. 

## **Cloud Deployment and Cost Estimate**
The estimated cost to run this system in production (24x7) for 30 days with 5 queries per day is approximately $5-10(INR450-INR850) on platforms like Render or DigitalOcean, leveraging their free or low-tier plans for containerized applications.
Deployed Solution Link: https://dice-dreams-reviews.onrender.com

## **Acknowledgments**
This project was developed with the assistance of various online resources, tools, and libraries to ensure a robust and functional solution.

**License**
## **Tools and Resources Used**
- ChatGPT (by OpenAI): ChatGPT was used to provide guidance, troubleshooting support, and code optimization for various aspects of the project. Specific guidance was provided on Flask setup, database configuration, handling Render deployment issues, and enhancing code modularity and readability.
- Google Play Scraper: The google-play-scraper library was utilized to scrape reviews from the Google Play Store for the Dice Dreams app, enabling regular updates to the review dataset.
- Flask: Flask was used to develop the REST API, providing endpoints for retrieving categorized reviews with filtering options.
- SQLAlchemy: SQLAlchemy served as the ORM for managing the SQLite database, enabling efficient storage and retrieval of review data.
- Render: Render's cloud deployment platform was chosen to host the containerized application, facilitating access to the service online.
- Docker: Docker was used to containerize the application, ensuring consistency in different environments and simplifying deployment.
- Each tool and library played an important role in building the final solution, and this project wouldn’t have been possible without these valuable resources. Special thanks to the ChatGPT model for assisting in 
 troubleshooting, code suggestions, and optimizing workflow design.

## **License**
This project is licensed under the MIT License.
