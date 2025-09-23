import React, { useState } from "react";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    crop: "",
    crop_year: "",
    season: "",
    state: "",
    area: "",
    production: "",
    annual_rainfall: "",
    fertilizer: "",
    pesticide: "",
    budget: ""
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error fetching recommendation:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1>AI-Powered Crop Yield & Recommendation</h1>
      <form onSubmit={handleSubmit} className="form-box">
        <label>Crop:</label>
        <input type="text" name="crop" value={formData.crop} onChange={handleChange} required />

        <label>Crop Year:</label>
        <input type="number" name="crop_year" value={formData.crop_year} onChange={handleChange} required />

        <label>Season:</label>
        <select name="season" value={formData.season} onChange={handleChange} required>
          <option value="">Select Season</option>
          <option value="Rabi">Rabi</option>
          <option value="Kharif">Kharif</option>
          <option value="Kharif">Whole Year</option>
          <option value="Kharif">Summer</option>
          <option value="Kharif">Winter</option>
          <option value="Kharif">Autumn</option>
        </select>

        <label>State:</label>
        <input type="text" name="state" value={formData.state} onChange={handleChange} required />

        <label>Area (ha):</label>
        <input type="number" name="area" value={formData.area} onChange={handleChange} required />

        <label>Production (tons):</label>
        <input type="number" name="production" value={formData.production} onChange={handleChange} required />

        <label>Annual Rainfall (mm):</label>
        <input type="number" name="annual_rainfall" value={formData.annual_rainfall} onChange={handleChange} required />

        <label>Fertilizer (kg):</label>
        <input type="number" name="fertilizer" value={formData.fertilizer} onChange={handleChange} required />

        <label>Pesticide (kg):</label>
        <input type="number" name="pesticide" value={formData.pesticide} onChange={handleChange} required />

        <label>Budget (INR):</label>
        <input type="number" name="budget" value={formData.budget} onChange={handleChange} required />

        <button type="submit" disabled={loading}>
          {loading ? "Processing..." : "Get Recommendation"}
        </button>
      </form>

      {result && (
        <div className="result-box">
          <h2>📊 Prediction Result</h2>
          <p><strong>Predicted Yield:</strong> {result.predicted_yield} t/ha</p>
          <h3>📝 Recommendation:</h3>
          <p>{result.recommendation}</p>
        </div>
      )}
    </div>
  );
}

export default App;