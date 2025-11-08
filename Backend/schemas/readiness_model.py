# Backend/schemas/readiness_models.py
from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Optional

class ReadinessBreakdownItem(BaseModel):
    score: int
    weight: int

class ReadinessResponse(BaseModel):
    score: int
    piti_low: int
    piti_high: int
    eta_weeks: int
    affordability_fit: int
    credit_band_points: int
    reserves_months: float
    pkt_points: int
    breakdown: Dict[str, ReadinessBreakdownItem]
    timeline: List[Dict[str, int | str]]

class ReadinessForm(BaseModel):
    # ✅ Added fields for user tracking & location
    user_id: Optional[str] = Field(None, description="User's unique Firestore UID")
    city_zip: str = Field(..., description="ZIP code")
    state: str = Field(..., description="State abbreviation")

    # Existing form fields
    income_net: float = Field(..., description="Monthly net income")
    credit_score: int = Field(..., description="FICO score")
    savings: float = 0
    dpa_amount: float = 0
    dp_pct: float = 3
    target_price_min: float = ...
    target_price_max: float = ...
    rent: float = 0
    debts_min: float = 0
    packet_completeness: float = 60  # 0-100
    city_zip: str = "27610"  # optional legacy fallback