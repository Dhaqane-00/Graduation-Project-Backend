from flask import Blueprint, jsonify
from pymongo import MongoClient
import logging
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

bp = Blueprint('summary_chart_data', __name__)


# Get the MongoDB URL from the environment variables
MONGODB_URL = os.getenv('MONGODB_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

# Initialize the MongoDB client with the Atlas connection string
client = MongoClient(MONGODB_URL)
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
                    'Scholarship': {'$gt': 0}
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
                    'Scholarship': {'$eq': 0}
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
    

@bp.route('/Re-exams-summary', methods=['GET'])
def get_graduates_dropouts_summary():
    try:
        pipeline = [
            {
                '$match': {
                    'NO-Re-exams': {'$gt': 0}
                }
            },
            {
                '$group': {
                    '_id': {
                        'Department': '$Department',
                        'Prediction': '$Prediction',
                        'ReExam': '$NO-Re-exams'
                    },
                    'count': {'$sum': 1}
                }
            },
            {
                '$group': {
                    '_id': '$_id.Department',
                    'details': {
                        '$push': {
                            'Prediction': '$_id.Prediction',
                            'ReExam': '$_id.NO-Re-exams',
                            'count': '$count'
                        }
                    },
                    'total': {'$sum': '$count'},
                    'total_graduated': {
                        '$sum': {
                            '$cond': [{'$eq': ['$_id.Prediction', 'Will Graduate']}, '$count', 0]
                        }
                    },
                    'total_dropout': {
                        '$sum': {
                            '$cond': [{'$eq': ['$_id.Prediction', 'Dropout']}, '$count', 0]
                        }
                    }
                }
            }
        ]
        graduates_dropouts_summary = list(predictions_collection.aggregate(pipeline))
        logging.info(f"Graduates and dropouts summary data fetched: {graduates_dropouts_summary}")
        return jsonify(graduates_dropouts_summary=graduates_dropouts_summary), 200
    except Exception as e:
        logging.error(f"Error fetching graduates and dropouts summary data: {e}")
        return jsonify(error=str(e)), 500
 