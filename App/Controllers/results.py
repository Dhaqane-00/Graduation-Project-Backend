from flask import Blueprint, jsonify
from pymongo import MongoClient
import logging

bp = Blueprint('results', __name__)

# Set up MongoDB connection
client = MongoClient('localhost', 27017)
db = client['predictions_db']
predictions_collection = db['predictions']

@bp.route('/results', methods=['GET'])
def get_results():
    try:
        results = list(predictions_collection.find({}, {"_id": 1, "Department": 1, "Gender": 1, "Mode": 1, "GPA": 1, "Prediction": 1}))
        for result in results:
            result['_id'] = str(result['_id'])
        logging.info(f"Results fetched: {results}")
        return jsonify(results=results), 200
    except Exception as e:
        logging.error(f"Error fetching results: {e}")
        return jsonify(error=str(e)), 500
