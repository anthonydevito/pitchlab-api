from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from . import models, schemas
from .database import engine, get_db

# Create tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PitchLab API", version="1.0.0")

@app.get("/")
def read_root():
    return {"status": "PitchLab API is active. Ready for bullpen data ingestion."}

@app.post("/pitchers/", response_model=schemas.Pitcher)
def create_pitcher(pitcher: schemas.PitcherCreate, db: Session = Depends(get_db)):
    """Creates a new pitcher profile in the database."""
    db_pitcher = models.Pitcher(name=pitcher.name, throws=pitcher.throws)
    db.add(db_pitcher)
    db.commit()
    db.refresh(db_pitcher)
    return db_pitcher

@app.get("/pitchers/{pitcher_id}", response_model=schemas.Pitcher)
def get_pitcher(pitcher_id: int, db: Session = Depends(get_db)):
    """Retrieves a pitcher and their full history of logged pitches."""
    db_pitcher = db.query(models.Pitcher).filter(models.Pitcher.id == pitcher_id).first()
    if db_pitcher is None:
        raise HTTPException(status_code=404, detail="Pitcher not found")
    return db_pitcher

@app.post("/pitchers/{pitcher_id}/sessions/", response_model=schemas.BullpenSession)
def add_bullpen_session(pitcher_id: int, session: schemas.BullpenSessionCreate, db: Session = Depends(get_db)):
    """Logs a new pitch for a specific pitcher."""
    # Verify pitcher exists
    db_pitcher = db.query(models.Pitcher).filter(models.Pitcher.id == pitcher_id).first()
    if db_pitcher is None:
        raise HTTPException(status_code=404, detail="Pitcher not found")
        
    db_session = models.BullpenSession(**session.model_dump(), pitcher_id=pitcher_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@app.get("/pitchers/{pitcher_id}/analytics")
def get_pitcher_analytics(pitcher_id: int, db: Session = Depends(get_db)):
    """
    Calculates the average velocity, spin rate, and IVB for each pitch type in a pitcher's arsenal.
    """
    # Verify pitcher exists
    db_pitcher = db.query(models.Pitcher).filter(models.Pitcher.id == pitcher_id).first()
    if db_pitcher is None:
        raise HTTPException(status_code=404, detail="Pitcher not found")

    # SQL aggregation
    results = db.query(
        models.BullpenSession.pitch_type,
        func.count(models.BullpenSession.id).label('pitch_count'),
        func.avg(models.BullpenSession.velocity_mph).label('avg_velocity'),
        func.avg(models.BullpenSession.spin_rate_rpm).label('avg_spin'),
        func.avg(models.BullpenSession.ivb_inches).label('avg_ivb')
    ).filter(models.BullpenSession.pitcher_id == pitcher_id)\
     .group_by(models.BullpenSession.pitch_type).all()

    # Format data
    arsenal_stats = []
    for row in results:
        arsenal_stats.append({
            "pitch_type": row.pitch_type,
            "usage_count": row.pitch_count,
            "avg_velocity_mph": round(row.avg_velocity, 1) if row.avg_velocity else 0.0,
            "avg_spin_rate_rpm": round(row.avg_spin, 0) if row.avg_spin else 0,
            "avg_ivb_inches": round(row.avg_ivb, 1) if row.avg_ivb else 0.0
        })

    return {
        "pitcher_name": db_pitcher.name,
        "total_pitches_logged": sum(stat["usage_count"] for stat in arsenal_stats),
        "arsenal_averages": arsenal_stats
    }
