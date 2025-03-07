import joblib
import numpy as np
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load trained model, scaler, and mappings
try:
    model = joblib.load("crop_recommendation_model.pkl")
    scaler = joblib.load("scaler.pkl")
    crop_mapping = joblib.load("crop_mapping.pkl")

    if not hasattr(scaler, "transform"):
        raise ValueError("Loaded scaler is not a StandardScaler instance.")
except Exception as e:
    print(f"❌ Error loading model or scaler: {e}")
    model, scaler, crop_mapping = None, None, {}

# Load crop details from JSON
try:
    with open("crop_details.json", "r") as file:
        crop_details = {key.lower(): value for key, value in json.load(file).items()}  # Lowercase keys

    print("✅ Loaded Crop Details:")
    print(json.dumps(crop_details, indent=2))  # Pretty-print JSON

except Exception as e:
    print(f"❌ Error loading crop details: {e}")
    crop_details = {}

@app.route('/')
def home():
    return "🌱 Crop Recommendation API is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided."})

        features = np.array([[data.get('N', 0), data.get('P', 0), data.get('K', 0), 
                              data.get('temperature', 0), data.get('humidity', 0), 
                              data.get('pH', 0), data.get('rainfall', 0)]])
        
        if scaler is None or model is None:
            return jsonify({"error": "Model or scaler not loaded. Try retraining the model."})

        scaled_features = scaler.transform(features)
        prediction = model.predict(scaled_features)

        predicted_crop = crop_mapping.get(prediction[0], "Unknown").lower()
        crop_info = crop_details.get(predicted_crop, {"info": "Details not available."})

        # Debugging logs
        print(f"🔍 Predicted Crop: {predicted_crop}")
        print(f"🌾 Crop Details Retrieved: {crop_info}")

        return jsonify({"recommended_crop": predicted_crop, "crop_details": crop_info})

    except Exception as e:
        print(f"❌ Error in prediction: {e}")
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
