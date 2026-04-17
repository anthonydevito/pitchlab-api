from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Pitcher(Base):
    __tablename__ = "pitchers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    throws = Column(String) # 'R' or 'L'
    
    # Establish relationship to the bullpen sessions table
    sessions = relationship("BullpenSession", back_populates="pitcher")

class BullpenSession(Base):
    __tablename__ = "bullpen_sessions"

    id = Column(Integer, primary_key=True, index=True)
    pitcher_id = Column(Integer, ForeignKey("pitchers.id"))
    pitch_type = Column(String, index=True) # ex.) 'Fastball' & 'Slider'
    velocity_mph = Column(Float)
    spin_rate_rpm = Column(Integer)
    ivb_inches = Column(Float) # ivb stands for Induced Vertical Break
    
    # Establish relationship back to the pitcher
    pitcher = relationship("Pitcher", back_populates="sessions")
