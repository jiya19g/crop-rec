import React, { useState } from "react";
import "./App.css"; // Import the CSS file

function App() {
  const [formData, setFormData] = useState({
    N: "",
    P: "",
    K: "",
    temperature: "",
    humidity: "",
    pH: "",
    rainfall: "",
  });

  const [crop, setCrop] = useState("");
  const [cropInfo, setCropInfo] = useState(null);
  const [error, setError] = useState("");

  // Handle input change
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Fetch crop recommendation
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setCropInfo(null);

    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error("Failed to fetch prediction");

      const data = await response.json();
      setCrop(data.recommended_crop);
      fetchCropInfo(data.recommended_crop); // Fetch additional crop info
    } catch (error) {
      console.error("Error:", error);
      setError("Error fetching prediction");
    }
  };

  // Fetch crop details from backend
  const fetchCropInfo = async (cropName) => {
    try {
      const response = await fetch(`http://localhost:5000/crop-info/${cropName.toLowerCase()}`);
      if (!response.ok) throw new Error("Failed to fetch crop info");

      const data = await response.json();
      setCropInfo(data.info);
    } catch (error) {
      console.error("Error fetching crop info:", error);
      setError("No additional information available.");
    }
  };

  return (
    <div className="container">
      <h1>🌱 Crop Recommendation System</h1>

      <form onSubmit={handleSubmit}>
        {["N", "P", "K", "temperature", "humidity", "pH", "rainfall"].map((field) => (
          <div key={field}>
            <label>{field}: </label>
            <input type="number" name={field} value={formData[field]} onChange={handleChange} required />
          </div>
        ))}

        <button type="submit">Predict Crop</button>
      </form>

      {crop && <h2 className="result">🌾 Recommended Crop: {crop}</h2>}

      {/* Show Crop Information */}
      {cropInfo && (
  <div className="crop-info">
    <h3>🌿 Crop Growth Information</h3>
    <ul>
      {Object.entries(cropInfo).map(([key, value]) => (
        <li key={key}>
          <strong>{key}:</strong> {value}
        </li>
      ))}
    </ul>
  </div>
)}


      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default App;
