import joblib
import numpy as np
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load trained model and scaler
try:
    model = joblib.load("crop_recommendation_model.pkl")
    scaler = joblib.load("scaler.pkl")

    if not hasattr(scaler, "transform"):
        raise ValueError("Loaded scaler is not a StandardScaler instance.")
except Exception as e:
    print(f"Error loading model or scaler: {e}")
    scaler = None

# Load crop growth info
try:
    with open("Crop_Growth_Info.json", "r") as file:
        crop_growth_info = json.load(file)
except Exception as e:
    print(f"Error loading Crop_Growth_Info.json: {e}")
    crop_growth_info = {}

# Load crop mapping
try:
    crop_mapping = joblib.load("crop_mapping.pkl")
except Exception as e:
    print(f"Error loading crop_mapping.pkl: {e}")
    crop_mapping = {}

@app.route('/')
def home():
    return "Crop Recommendation API is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = np.array([[data['N'], data['P'], data['K'], data['temperature'], 
                              data['humidity'], data['pH'], data['rainfall']]])

        if scaler:
            scaled_features = scaler.transform(features)
        else:
            return jsonify({"error": "Scaler not loaded properly. Try retraining the model."})

        prediction = model.predict(scaled_features)
        
        predicted_crop = crop_mapping.get(prediction[0], "Unknown Crop")

        # Get crop growth info for the predicted crop
        crop_info = crop_growth_info.get(predicted_crop.lower(), "No additional info available")

        return jsonify({"recommended_crop": predicted_crop, "crop_info": crop_info})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/crop-info/<crop_name>', methods=['GET'])
def get_crop_info(crop_name):
    crop_name = crop_name.strip().lower()  # Normalize case
    crop_info = crop_growth_info.get(crop_name, "No additional info available")
    return jsonify({"info": crop_info})

if __name__ == '__main__':
    app.run(debug=True)
