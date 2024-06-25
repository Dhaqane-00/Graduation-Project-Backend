from flask import Blueprint, jsonify
from pymongo import MongoClient
import logging
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

bp = Blueprint('chart_data', __name__)


# Get the MongoDB URL from the environment variables
MONGODB_URL = os.getenv('MONGODB_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

# Initialize the MongoDB client with the Atlas connection string
client = MongoClient(MONGODB_URL)
db = client['predictions_db']
predictions_collection = db['predictions']

@bp.route('/chart-data', methods=['GET'])
def get_chart_data():
    try:
        pipeline = [
            {
                '$project': {
                    'Department': 1,
                    'Prediction': 1,
                    'Sex': {'$toLower': '$Sex'},
                    'Mode': 1
                }
            },
            {
                '$group': {
                    '_id': {
                        'Department': '$Department',
                        'Prediction': '$Prediction',
                        'Sex': '$Sex',
                        'Mode': '$Mode'
                    },
                    'count': {'$sum': 1}
                }
            },
            {
                '$group': {
                    '_id': '$_id.Department',
                    'predictions': {
                        '$push': {
                            'Prediction': '$_id.Prediction',
                            'Sex': '$_id.Sex',
                            'Mode': '$_id.Mode',
                            'count': '$count'
                        }
                    },
                    'total': {'$sum': '$count'}
                }
            }
        ]
        chart_data = list(predictions_collection.aggregate(pipeline))
        logging.info(f"Chart data fetched: {chart_data}")
        return jsonify(chart_data=chart_data), 200
    except Exception as e:
        logging.error(f"Error fetching chart data: {e}")
        return jsonify(error=str(e)), 500
