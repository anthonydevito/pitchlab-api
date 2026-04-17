from pydantic import BaseModel
from typing import List

# --- Bullpen Session Schemas ---
class BullpenSessionBase(BaseModel):
    pitch_type: str
    velocity_mph: float
    spin_rate_rpm: int
    ivb_inches: float

class BullpenSessionCreate(BullpenSessionBase):
    pass

class BullpenSession(BullpenSessionBase):
    id: int
    pitcher_id: int

    class Config:
        from_attributes = True

# --- Pitcher Schemas ---
class PitcherBase(BaseModel):
    name: str
    throws: str

class PitcherCreate(PitcherBase):
    pass

class Pitcher(PitcherBase):
    id: int
    sessions: List[BullpenSession] = []

    class Config:
        from_attributes = True
