import React, { useState } from "react";
import "./App.css";

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
  const [cropDetails, setCropDetails] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Submitting form data:", formData);

    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      console.log("Response status:", response.status);

      if (!response.ok) throw new Error("Failed to fetch data");

      const data = await response.json();
      console.log("Response data:", data);
      setCrop(data.recommended_crop || "Error fetching prediction");
      setCropDetails(data.crop_details || null);
    } catch (error) {
      console.error("Error:", error);
      setCrop("Error fetching prediction");
      setCropDetails(null);
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

      {crop && cropDetails && Object.keys(cropDetails).length > 0 ? (
  <div className="crop-info">
    <h3>🌍 Crop Details:</h3>
    <p><strong>Growing Season:</strong> {cropDetails.season || "N/A"}</p>
    <p><strong>Soil Type:</strong> {cropDetails.soil || "N/A"}</p>
    <p><strong>Water Requirement:</strong> {cropDetails.water_requirement || "N/A"}</p>
    <p><strong>Temperature:</strong> {cropDetails.temperature || "N/A"}</p>
    <p><strong>Growing Period:</strong> {cropDetails.growing_period || "N/A"}</p>
  </div>
) : crop ? (
  <p>No crop details available.</p>
) : null}

    </div>
  );
}

export default App;
