import joblib
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load trained model and scaler
try:
    model = joblib.load("crop_recommendation_model.pkl")
    scaler = joblib.load("scaler.pkl")

    # Ensure the scaler is an instance of StandardScaler
    if not hasattr(scaler, "transform"):
        raise ValueError("Loaded scaler is not a StandardScaler instance.")
except Exception as e:
    print(f"Error loading model or scaler: {e}")
    scaler = None

@app.route('/')
def home():
    return "Crop Recommendation API is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data
        data = request.get_json()

        # Extract features
        features = np.array([[data['N'], data['P'], data['K'], data['temperature'], 
                              data['humidity'], data['pH'], data['rainfall']]])

        # Apply scaling if scaler is loaded
        if scaler:
            scaled_features = scaler.transform(features)
        else:
            return jsonify({"error": "Scaler not loaded properly. Try retraining the model."})

        # Predict the crop
        prediction = model.predict(scaled_features)
        
        # Convert numerical prediction back to crop name
        crop_mapping = joblib.load("crop_mapping.pkl")  # Load the mapping dictionary
        predicted_crop = crop_mapping[prediction[0]]

        return jsonify({"recommended_crop": predicted_crop})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
