"""Optional unsupervised demo: flags unusual records, not malnutrition."""
import numpy as np
from sklearn.ensemble import IsolationForest

FEATURES = ["age_years", "height_cm", "weight_kg", "bmi"]

def fit_demo_detector(rows):
    """Fit only when enough records exist. Output is an anomaly flag, not a risk diagnosis."""
    if len(rows) < 10:
        return None
    matrix = np.array([[float(r[k]) for k in FEATURES] for r in rows], dtype=float)
    model = IsolationForest(contamination=0.10, random_state=42)
    model.fit(matrix)
    return model

def flag_record(model, row):
    if model is None:
        return {"available": False, "is_unusual": None,
                "message": "At least 10 saved records are needed for the demo anomaly detector."}
    values = np.array([[float(row[k]) for k in FEATURES]], dtype=float)
    unusual = bool(model.predict(values)[0] == -1)
    return {"available": True, "is_unusual": unusual,
            "message": "Unusual measurement pattern for this dataset; review data quality and context."
                       if unusual else "No unusual pattern detected by the demo model."}
