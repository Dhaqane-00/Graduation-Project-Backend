from flask import Blueprint, jsonify
from pymongo import MongoClient
import logging

bp = Blueprint('chart_data', __name__)

# Set up MongoDB connection
client = MongoClient('localhost', 27017)
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
