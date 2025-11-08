# Backend/services/readiness_service.py
from typing import Dict, List, Literal
from Backend.schemas.readiness_model import ReadinessResponse, ReadinessBreakdownItem, ReadinessForm

CREDIT_THRESHOLD = 640
AFFORDABILITY_MIN = 0.28
AFFORDABILITY_MAX = 0.38

def calculate_piti(home_price: float, down_payment_pct: float, zip_code: str = "27610") -> Dict[str, int]:
    loan_amount = home_price * (1 - down_payment_pct / 100.0)
    monthly_rate = 0.07 / 12.0  # 7% APR assumption
    months = 360
    if loan_amount <= 0:
        return {"low": 0, "high": 0}
    pi = loan_amount * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    property_tax = (home_price * 0.0085) / 12.0
    insurance = home_price * 0.0035 / 12.0
    piti = pi + property_tax + insurance
    return {"low": round(piti * 0.95), "high": round(piti * 1.05)}

def calculate_affordability_fit(piti_mid: float, net_income: float) -> int:
    if net_income <= 0:
        return 0
    ratio = piti_mid / net_income
    if ratio < AFFORDABILITY_MIN:
        return 100
    if ratio > AFFORDABILITY_MAX:
        return 0
    rng = AFFORDABILITY_MAX - AFFORDABILITY_MIN
    pos = ratio - AFFORDABILITY_MIN
    return round(100 * (1 - pos / rng))

def calculate_credit_points(credit_score: int) -> int:
    if credit_score >= CREDIT_THRESHOLD:
        return 100
    if credit_score < 580:
        return 0
    return round(((credit_score - 580) / (CREDIT_THRESHOLD - 580)) * 100)

def calculate_reserves_points(savings: float, dpa_amount: float, piti_mid: float) -> int:
    if piti_mid <= 0:
        return 0
    total_reserves = savings + dpa_amount
    months_of_piti = total_reserves / piti_mid
    if months_of_piti >= 2:
        return 100
    if months_of_piti <= 0:
        return 0
    return round((months_of_piti / 2.0) * 100)

def calculate_packet_points(completeness: float) -> int:
    completeness = max(0, min(100, completeness))
    return round(completeness)

def generate_timeline(eta_weeks: int) -> List[Dict[str, int | str]]:
    milestones = [
        {"id": "budget", "title": "Budget Set", "weeks": 0},
        {"id": "dpa", "title": "DPA Pre-Check", "weeks": 1},
        {"id": "docs", "title": "Docs 80%", "weeks": min(3, int(eta_weeks * 0.3))},
        {"id": "credit", "title": "Credit Tune-Up", "weeks": min(6, int(eta_weeks * 0.5))},
        {"id": "packet", "title": "Lender-Ready Packet", "weeks": int(eta_weeks * 0.8)},
        {"id": "preapproval", "title": "Pre-Approval Window", "weeks": eta_weeks},
        {"id": "appraisal", "title": "Appraisal Prep", "weeks": eta_weeks + 2},
    ]
    out = []
    for i, m in enumerate(milestones):
        status: Literal["completed", "current", "upcoming"] = "completed" if i == 0 else ("current" if i == 1 else "upcoming")
        out.append({**m, "status": status})
    return out

def compute_readiness(body: ReadinessForm) -> ReadinessResponse:
    target_price = (body.target_price_min + body.target_price_max) / 2.0
    piti = calculate_piti(target_price, body.dp_pct, body.city_zip)
    piti_mid = (piti["low"] + piti["high"]) / 2.0

    affordability = calculate_affordability_fit(piti_mid, body.income_net)
    credit = calculate_credit_points(body.credit_score)
    reserves = calculate_reserves_points(body.savings, body.dpa_amount, piti_mid)
    packet = calculate_packet_points(body.packet_completeness)

    score = round(
        affordability * 0.40 +
        credit * 0.25 +
        reserves * 0.20 +
        packet * 0.15
    )

    down_payment = target_price * (body.dp_pct / 100.0)
    closing_costs = target_price * 0.03
    reserves_needed = piti_mid * 2.0
    total_cash = down_payment + closing_costs + reserves_needed
    cash_gap = max(0.0, total_cash - body.savings - body.dpa_amount)
    weekly_surplus = (body.income_net - body.rent - body.debts_min) / 4.33 if body.income_net > 0 else 0
    cash_weeks = int((cash_gap / max(weekly_surplus, 100)) + 0.999) if cash_gap > 0 else 0
    credit_weeks = 0 if body.credit_score >= CREDIT_THRESHOLD else 6
    packet_weeks = int(((100 - body.packet_completeness) / 10.0) + 0.999)
    eta_weeks = max(cash_weeks, credit_weeks, packet_weeks)

    timeline = generate_timeline(eta_weeks)

    return ReadinessResponse(
        score=score,
        piti_low=piti["low"],
        piti_high=piti["high"],
        eta_weeks=eta_weeks,
        affordability_fit=affordability,
        credit_band_points=credit,
        reserves_months=(body.savings / piti_mid) if piti_mid > 0 else 0.0,
        pkt_points=packet,
        breakdown={
            "affordability": ReadinessBreakdownItem(score=affordability, weight=40),
            "credit": ReadinessBreakdownItem(score=credit, weight=25),
            "reserves": ReadinessBreakdownItem(score=reserves, weight=20),
            "packet": ReadinessBreakdownItem(score=packet, weight=15),
        },
        timeline=timeline,
    )
