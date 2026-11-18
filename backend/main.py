from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import Base, engine, get_db
from .models import Assessment
from .schemas import AssessmentCreate
from .analysis import calculate_bmi, assess_measurement
from .ml_anomaly import fit_demo_detector, flag_record

Base.metadata.create_all(bind=engine)
app = FastAPI(title="NutriTrack API", version="1.0.0",
              description="Educational nutritional data screening-support prototype.")
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False,
                   allow_methods=["*"], allow_headers=["*"])

@app.get("/api/health")
def health():
    return {"status": "ok", "application": "NutriTrack"}

@app.post("/api/assessments", status_code=201)
def create_assessment(payload: AssessmentCreate, db: Session = Depends(get_db)):
    bmi = calculate_bmi(payload.height_cm, payload.weight_kg)
    status, message = assess_measurement(payload.age_years, bmi)
    record = Assessment(**payload.model_dump(), bmi=bmi,
                        indicator_status=status, indicator_message=message)
    db.add(record)
    db.commit()
    db.refresh(record)
    return serialize(record)

@app.get("/api/assessments")
def list_assessments(db: Session = Depends(get_db)):
    rows = db.query(Assessment).order_by(Assessment.created_at.desc()).all()
    return [serialize(r) for r in rows]

@app.get("/api/summary")
def summary(db: Session = Depends(get_db)):
    total = db.query(func.count(Assessment.id)).scalar() or 0
    return {"total_assessments": total,
            "under_20_records": db.query(func.count(Assessment.id)).filter(Assessment.age_years < 20).scalar() or 0,
            "adult_records": db.query(func.count(Assessment.id)).filter(Assessment.age_years >= 20).scalar() or 0}

@app.get("/api/ml/status")
def ml_status(db: Session = Depends(get_db)):
    rows = db.query(Assessment).all()
    data = [{"age_years": r.age_years, "height_cm": r.height_cm,
             "weight_kg": r.weight_kg, "bmi": r.bmi} for r in rows]
    model = fit_demo_detector(data)
    if not data:
        return {"available": False, "message": "Add at least 10 records to enable the demo anomaly detector."}
    result = flag_record(model, data[0])
    return {"available": result["available"], "message": result["message"],
            "purpose": "Dataset anomaly exploration only; not a malnutrition prediction."}

@app.delete("/api/assessments/{record_id}", status_code=204)
def delete_assessment(record_id: int, db: Session = Depends(get_db)):
    row = db.query(Assessment).filter(Assessment.id == record_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Assessment not found")
    db.delete(row)
    db.commit()

def serialize(r):
    return {"id": r.id, "participant_code": r.participant_code, "age_years": r.age_years,
            "sex_reference": r.sex_reference, "height_cm": r.height_cm, "weight_kg": r.weight_kg,
            "bmi": r.bmi, "indicator_status": r.indicator_status,
            "indicator_message": r.indicator_message,
            "created_at": r.created_at.isoformat() if isinstance(r.created_at, datetime) else str(r.created_at)}
