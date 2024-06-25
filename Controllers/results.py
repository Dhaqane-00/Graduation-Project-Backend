from flask import Blueprint, jsonify
from pymongo import MongoClient
import logging
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

bp = Blueprint('results', __name__)


# Get the MongoDB URL from the environment variables
MONGODB_URL = os.getenv('MONGODB_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

# Initialize the MongoDB client with the Atlas connection string
client = MongoClient(MONGODB_URL)
db = client['predictions_db']
predictions_collection = db['predictions']

@bp.route('/results', methods=['GET'])
def get_results():
    try:
        # Fetch results from MongoDB including additional fields
        results = list(predictions_collection.find({}, {
            "_id": 1,
            "Department": 1,
            "Sex": 1,  # Adjusted from "Gender" to "Sex"
            "Mode": 1,
            "Att-S1": 1,
            "Att-S2": 1,
            "Att-S3": 1,
            "Att-S4": 1,
            "Att-S5": 1,
            "Att-S6": 1,
            "Att-S7": 1,
            "Att-S8": 1,
            "Schollarship": 1,
            "NO-Re-exams": 1,
            "GPA-S1": 1,
            "GPA-S2": 1,
            "GPA-S3": 1,
            "GPA-S4": 1,
            "GPA-S5": 1,
            "GPA-S6": 1,
            "GPA-S7": 1,
            "GPA-S8": 1,
            "Prediction": 1
        }))

        # Convert ObjectId to string for JSON serialization
        for result in results:
            result['_id'] = str(result['_id'])

        # Logging successful fetch
        logging.info(f"Results fetched: {results}")

        # Return results as JSON response
        return jsonify(results=results), 200

    except Exception as e:
        # Log error details
        logging.error(f"Error fetching results: {e}")
        
        # Return error response
        return jsonify(error=str(e)), 500
