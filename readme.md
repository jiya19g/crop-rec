# Crop Recommendation System

## Overview
The **Crop Recommendation System** is an AI-powered application that suggests the best crops to grow based on soil and environmental parameters. The system leverages an **XGBoost model** trained with a **Standard Scaler** for feature scaling and is built with a **Flask backend** and a **React frontend** for seamless user interaction.

## Features
- **Machine Learning Model**: Trained using XGBoost with Standard Scaler for improved accuracy.
- **Input Parameters**: Nitrogen (N), Phosphorus (P), Potassium (K), Temperature, Humidity, pH, and Rainfall.
- **Backend**: Flask-based API to handle predictions.
- **Frontend**: React-based UI for user-friendly interaction.
- **Real-time Recommendations**: Predicts the most suitable crop based on user inputs.

## Tech Stack
- **Machine Learning**: Python, XGBoost, Standard Scaler
- **Backend**: Flask
- **Frontend**: React.js
- **Others**: Pandas, NumPy, Scikit-learn

## Installation
### Prerequisites
Ensure you have **Python (3.8+), Node.js (14+), and pip** installed.

### Setup Backend
```sh
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Setup Frontend
```sh
cd frontend
npm install
npm start
```

## Usage
1. Open the web application.
2. Enter soil and weather parameters.
3. Get the recommended crop instantly.

## Folder Structure
```
├── backend
│   ├── app.py                            # Flask backend
│   ├── Crop_Growth_Info.json             # Crop growth data
│   ├── crop_mapping.pkl                   # Crop mapping model
│   ├── crop_recommendation_model.pkl      # Trained XGBoost model
│   ├── scaler.pkl                          # Standard Scaler
│   ├── requirements.txt                   # Dependencies
│
├── frontend
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── App.css
│   │   ├── App.js                          # Main component
│   │   ├── App.test.js
│   │   ├── index.css
│   │   ├── index.js                         # Entry point
│   │   ├── logo.svg
│   │   ├── reportWebVitals.js
│   │   ├── setupTests.js
│   ├── package-lock.json
│   ├── package.json                        # Dependencies
│
├── venv/                                  # Virtual environment
├── .gitignore
├── README.md
```

## License
This project is **MIT licensed**.
