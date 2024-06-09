from flask import Blueprint, jsonify
from pymongo import MongoClient
import logging

bp = Blueprint('summary_chart_data', __name__)

# Set up MongoDB connection
client = MongoClient('localhost', 27017)
db = client['predictions_db']
predictions_collection = db['predictions']

@bp.route('/summary-chart-data', methods=['GET'])
def get_summary_chart_data():
    try:
        pipeline = [
            {
                '$group': {
                    '_id': {
                        'Prediction': '$Prediction',
                        'Gender': '$Gender',
                        'Mode': '$Mode'
                    },
                    'count': {'$sum': 1}
                }
            },
            {
                '$group': {
                    '_id': '$_id.Prediction',
                    'genders': {
                        '$push': {
                            'Gender': '$_id.Gender',
                            'Mode': '$_id.Mode',
                            'count': '$count'
                        }
                    },
                    'total': {'$sum': '$count'}
                }
            }
        ]
        summary_data = list(predictions_collection.aggregate(pipeline))
        logging.info(f"Summary chart data fetched: {summary_data}")
        return jsonify(summary_data=summary_data), 200
    except Exception as e:
        logging.error(f"Error fetching summary chart data: {e}")
        return jsonify(error=str(e)), 500
