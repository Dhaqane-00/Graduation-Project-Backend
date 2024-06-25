from flask import Blueprint, request, jsonify
import pandas as pd
import joblib
import logging
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

bp = Blueprint('predict', __name__)

# Load the saved encoders, scaler, and model
label_encoder_sex = joblib.load('Models/label_encoder_sex_many.pkl')
label_encoder_mode = joblib.load('Models/label_encoder_mode_many.pkl')
column_transformer = joblib.load('Models/ColumnTransformer_many.pkl')
sc = joblib.load('Models/StandardScaler_many.pkl')
model = joblib.load('Models/model_many.pkl')

# Get the MongoDB URL from the environment variables
MONGODB_URL = os.getenv('MONGODB_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

# Initialize the MongoDB client with the Atlas connection string
client = MongoClient(MONGODB_URL)
db = client['predictions_db']
predictions_collection = db['predictions']

@bp.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    
    try:
        input_data = pd.read_csv(file)
        logging.info(f"Input data columns: {input_data.columns.tolist()}")
        logging.info(f"Input data shape: {input_data.shape}")

        input_data['Sex'] = label_encoder_sex.transform(input_data['Sex'])
        input_data['Mode'] = label_encoder_mode.transform(input_data['Mode'])
        logging.info(f"Data after encoding: {input_data.head()}")

        transformed_data = column_transformer.transform(input_data)
        logging.info(f"Transformed data shape: {transformed_data.shape}")

        transformed_data = sc.transform(transformed_data)
        predictions = model.predict(transformed_data)
        input_data['Prediction'] = ["Will Graduate" if pred == 1 else "Dropout" for pred in predictions]

        input_data['Sex'] = label_encoder_sex.inverse_transform(input_data['Sex'])
        input_data['Mode'] = label_encoder_mode.inverse_transform(input_data['Mode'])

        result = input_data.to_dict(orient='records')
        predictions_collection.delete_many({})
        predictions_collection.insert_many(result)

        return jsonify(message="Predictions stored in database"), 200
    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        return jsonify(error=str(e)), 500