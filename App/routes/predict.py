from flask import Blueprint, request, jsonify
import pandas as pd
import joblib
import logging
from pymongo import MongoClient

bp = Blueprint('predict', __name__)

# Load the saved encoders, scaler, and model
label_encoder_gender = joblib.load('label_encoder_gender.pkl')
label_encoder_mode = joblib.load('label_encoder_mode.pkl')
column_transformer = joblib.load('ColumnTransformer.pkl')
sc = joblib.load('StandardScaler.pkl')
model = joblib.load('model.pkl')

# Set up MongoDB connection
client = MongoClient('localhost', 27017)
db = client['predictions_db']
predictions_collection = db['predictions']

@bp.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    
    try:
        input_data = pd.read_csv(file)
        logging.info(f"Input data columns: {input_data.columns.tolist()}")
        logging.info(f"Input data shape: {input_data.shape}")

        input_data['Gender'] = label_encoder_gender.transform(input_data['Gender'])
        input_data['Mode'] = label_encoder_mode.transform(input_data['Mode'])
        logging.info(f"Data after encoding: {input_data.head()}")

        transformed_data = column_transformer.transform(input_data)
        logging.info(f"Transformed data shape: {transformed_data.shape}")

        transformed_data = sc.transform(transformed_data)
        predictions = model.predict(transformed_data)
        input_data['Prediction'] = ["Will Graduate" if pred == 1 else "Dropout" for pred in predictions]

        input_data['Gender'] = label_encoder_gender.inverse_transform(input_data['Gender'])
        input_data['Mode'] = label_encoder_mode.inverse_transform(input_data['Mode'])

        result = input_data.to_dict(orient='records')
        predictions_collection.delete_many({})
        predictions_collection.insert_many(result)

        return jsonify(message="Predictions stored in database"), 200
    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        return jsonify(error=str(e)), 500
