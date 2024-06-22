from flask import Blueprint, request, jsonify
import pandas as pd
import joblib
import logging

bp = Blueprint('single_predict', __name__)

# Load the saved encoders, scaler, and model
label_encoder_sex = joblib.load('Models/label_encoder_sex_single.pkl')
label_encoder_mode = joblib.load('Models/label_encoder_mode_single.pkl')
column_transformer = joblib.load('Models/ColumnTransformer_single.pkl')
sc = joblib.load('Models/StandardScaler_single.pkl')
model = joblib.load('Models/model_single.pkl')

@bp.route('/single-predict', methods=['POST'])
def single_predict():
    data = request.json

    try:
        input_data = pd.DataFrame([data])
        logging.info(f"Input data: {input_data}")

        input_data['Sex'] = label_encoder_sex.transform(input_data['Sex'])
        input_data['Mode'] = label_encoder_mode.transform(input_data['Mode'])
        logging.info(f"Data after encoding: {input_data}")

        transformed_data = column_transformer.transform(input_data)
        logging.info(f"Transformed data: {transformed_data}")

        transformed_data = sc.transform(transformed_data)
        prediction = model.predict(transformed_data)[0]
        prediction_label = "Will Graduate" if prediction == 1 else "Dropout"

        return jsonify(prediction=prediction_label), 200
    except Exception as e:
        logging.error(f"Error in single prediction: {e}")
        return jsonify(error=str(e)), 500