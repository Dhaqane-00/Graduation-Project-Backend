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
                '$project': {
                    'Prediction': 1,
                    'Sex': {'$toLower': '$Sex'},
                    'Mode': 1
                }
            },
            {
                '$group': {
                    '_id': {
                        'Prediction': '$Prediction',
                        'Sex': '$Sex',
                        'Mode': '$Mode'
                    },
                    'count': {'$sum': 1}
                }
            },
            {
                '$group': {
                    '_id': '$_id.Prediction',
                    'details': {
                        '$push': {
                            'Sex': '$_id.Sex',
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
 
@bp.route('/Schollarship-summary', methods=['GET'])
def get_scholarship_summary():
    try:
        # Pipeline for students with scholarships
        pipeline_with_scholarship = [
            {
                '$match': {
                    'Schollarship': {'$gt': 0}
                }
            },
            {
                '$group': {
                    '_id': '$Prediction',
                    'count': {'$sum': 1}
                }
            }
        ]

        # Pipeline for students without scholarships
        pipeline_without_scholarship = [
            {
                '$match': {
                    'Schollarship': {'$eq': 0}
                }
            },
            {
                '$group': {
                    '_id': '$Prediction',
                    'count': {'$sum': 1}
                }
            }
        ]

        with_scholarship_summary = list(predictions_collection.aggregate(pipeline_with_scholarship))
        without_scholarship_summary = list(predictions_collection.aggregate(pipeline_without_scholarship))

        logging.info(f"Scholarship summary data fetched: {with_scholarship_summary}, {without_scholarship_summary}")

        return jsonify(
            with_scholarship_summary=with_scholarship_summary,
            without_scholarship_summary=without_scholarship_summary
        ), 200
    except Exception as e:
        logging.error(f"Error fetching scholarship summary data: {e}")
        return jsonify(error=str(e)), 500
    

@bp.route('/department-summary', methods=['GET'])
def get_department_summary():
    try:
        pipeline = [
            {
                '$group': {
                    '_id': {
                        'Department': '$Department',
                        'Prediction': '$Prediction'
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
                            'count': '$count'
                        }
                    },
                    'total': {'$sum': '$count'}
                }
            }
        ]
        department_summary = list(predictions_collection.aggregate(pipeline))
        logging.info(f"Department summary data fetched: {department_summary}")
        return jsonify(department_summary=department_summary), 200
    except Exception as e:
        logging.error(f"Error fetching department summary data: {e}")
        return jsonify(error=str(e)), 500
