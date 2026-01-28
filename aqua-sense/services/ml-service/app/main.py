"""
AquaSense ML Service
Provides machine learning capabilities for water quality prediction and anomaly detection
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
from datetime import datetime
import joblib
import os

app = FastAPI(title="AquaSense ML Service", version="1.0.0")

# Models directory
MODELS_DIR = os.getenv("MODEL_PATH", "/app/models")

class SensorReading(BaseModel):
    """Sensor reading data model"""
    sensor_id: str
    ph: float
    temperature: float
    turbidity: float
    dissolved_oxygen: float
    conductivity: float
    timestamp: datetime

class PredictionRequest(BaseModel):
    """Prediction request model"""
    readings: List[SensorReading]

class PredictionResponse(BaseModel):
    """Prediction response model"""
    predictions: List[dict]
    model_version: str
    confidence: float

class AnomalyDetectionRequest(BaseModel):
    """Anomaly detection request"""
    readings: List[SensorReading]

class AnomalyDetectionResponse(BaseModel):
    """Anomaly detection response"""
    anomalies: List[dict]
    anomaly_score: float

# Mock model for demonstration
class WaterQualityModel:
    """Water quality prediction model"""
    
    def __init__(self):
        self.version = "1.0.0"
    
    def predict(self, features: np.ndarray) -> np.ndarray:
        """Predict water quality based on sensor readings"""
        # Simple rule-based prediction for demonstration
        predictions = []
        for reading in features:
            ph, temp, turbidity, do, conductivity = reading
            
            # Quality score (0-100)
            score = 100
            
            # pH check (optimal: 6.5-8.5)
            if ph < 6.5 or ph > 8.5:
                score -= 20
            
            # Temperature check (optimal: 15-25°C)
            if temp < 15 or temp > 25:
                score -= 15
            
            # Turbidity check (lower is better)
            if turbidity > 5:
                score -= 25
            
            # Dissolved oxygen check (optimal: > 5 mg/L)
            if do < 5:
                score -= 30
            
            # Conductivity check
            if conductivity > 1000:
                score -= 10
            
            quality = "excellent" if score >= 80 else "good" if score >= 60 else "fair" if score >= 40 else "poor"
            
            predictions.append({
                "quality_score": max(0, score),
                "quality_level": quality,
                "risk_level": "low" if score >= 70 else "medium" if score >= 50 else "high"
            })
        
        return predictions

class AnomalyDetector:
    """Anomaly detection model"""
    
    def __init__(self):
        self.version = "1.0.0"
    
    def detect(self, features: np.ndarray) -> List[dict]:
        """Detect anomalies in sensor readings"""
        anomalies = []
        
        for idx, reading in enumerate(features):
            ph, temp, turbidity, do, conductivity = reading
            anomaly_flags = []
            
            # Check for anomalies
            if ph < 4 or ph > 10:
                anomaly_flags.append("extreme_ph")
            if temp < 0 or temp > 40:
                anomaly_flags.append("extreme_temperature")
            if turbidity > 50:
                anomaly_flags.append("high_turbidity")
            if do < 2:
                anomaly_flags.append("low_oxygen")
            if conductivity > 2000:
                anomaly_flags.append("high_conductivity")
            
            if anomaly_flags:
                anomalies.append({
                    "reading_index": idx,
                    "anomaly_types": anomaly_flags,
                    "severity": "high" if len(anomaly_flags) > 2 else "medium" if len(anomaly_flags) > 1 else "low"
                })
        
        return anomalies

# Initialize models
quality_model = WaterQualityModel()
anomaly_detector = AnomalyDetector()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ml-service",
        "version": "1.0.0",
        "models_loaded": True
    }

@app.post("/predict/water-quality", response_model=PredictionResponse)
async def predict_water_quality(request: PredictionRequest):
    """Predict water quality based on sensor readings"""
    try:
        # Extract features from readings
        features = np.array([
            [r.ph, r.temperature, r.turbidity, r.dissolved_oxygen, r.conductivity]
            for r in request.readings
        ])
        
        # Make predictions
        predictions = quality_model.predict(features)
        
        # Add sensor IDs to predictions
        for idx, pred in enumerate(predictions):
            pred["sensor_id"] = request.readings[idx].sensor_id
            pred["timestamp"] = request.readings[idx].timestamp.isoformat()
        
        return PredictionResponse(
            predictions=predictions,
            model_version=quality_model.version,
            confidence=0.92
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/detect/anomalies", response_model=AnomalyDetectionResponse)
async def detect_anomalies(request: AnomalyDetectionRequest):
    """Detect anomalies in sensor readings"""
    try:
        # Extract features from readings
        features = np.array([
            [r.ph, r.temperature, r.turbidity, r.dissolved_oxygen, r.conductivity]
            for r in request.readings
        ])
        
        # Detect anomalies
        anomalies = anomaly_detector.detect(features)
        
        # Add sensor information
        for anomaly in anomalies:
            idx = anomaly["reading_index"]
            anomaly["sensor_id"] = request.readings[idx].sensor_id
            anomaly["timestamp"] = request.readings[idx].timestamp.isoformat()
        
        # Calculate overall anomaly score
        anomaly_score = len(anomalies) / len(request.readings) if request.readings else 0
        
        return AnomalyDetectionResponse(
            anomalies=anomalies,
            anomaly_score=round(anomaly_score, 3)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection error: {str(e)}")

@app.get("/models/info")
async def get_model_info():
    """Get information about loaded models"""
    return {
        "water_quality_model": {
            "version": quality_model.version,
            "type": "rule-based",
            "features": ["ph", "temperature", "turbidity", "dissolved_oxygen", "conductivity"]
        },
        "anomaly_detector": {
            "version": anomaly_detector.version,
            "type": "statistical",
            "features": ["ph", "temperature", "turbidity", "dissolved_oxygen", "conductivity"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8086)
