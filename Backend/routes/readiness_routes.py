# from fastapi import APIRouter
# from Backend.schemas.readiness_model import ReadinessForm, ReadinessResponse
# from Backend.services.readiness_service import compute_readiness

# router = APIRouter(prefix="/readiness", tags=["readiness"])

# @router.post("/", response_model=ReadinessResponse)
# async def get_readiness_score(body: ReadinessForm):
#     """
#     POST /api/v1/readiness
#     Receives user's financial info and returns readiness metrics.
#     """
#     return compute_readiness(body)


from fastapi import APIRouter, HTTPException
from datetime import datetime
from Backend.schemas.readiness_model import ReadinessForm, ReadinessResponse
from Backend.services.readiness_service import compute_readiness
from Backend.config.firebase_config import db

router = APIRouter(prefix="/readiness", tags=["readiness"])

@router.post("/", response_model=ReadinessResponse)
async def get_readiness_score(body: ReadinessForm):
    """
    POST /api/v1/readiness
    - Receives user's financial info
    - Computes readiness score
    - Creates or updates readiness_profile in Firestore
    - Returns readiness metrics to the frontend
    """
    try:
        # --- Compute readiness ---
        result = compute_readiness(body)

        # --- Prepare data payload ---
        readiness_profile = {
            "city_zip": body.city_zip,
            "state": body.state,
            "income": body.income_net,
            "current_rent": body.rent,
            "monthly_debts": body.debts_min,
            "savings": body.savings,
            "dpa_funds": body.dpa_amount,
            "credit_score": body.credit_score,
            "target_price_min": body.target_price_min,
            "target_price_max": body.target_price_max,
            "down_payment_percent": body.dp_pct,
            "readiness_score": result.score,
            "piti_low": result.piti_low,
            "piti_high": result.piti_high,
            "eta_weeks": result.eta_weeks,
            "affordability_fit": result.affordability_fit,
            "updated_at": datetime.utcnow().isoformat(),
        }

        # --- Update or create in Firestore ---
        if not getattr(body, "user_id", None):
            raise HTTPException(status_code=400, detail="user_id is required to save readiness data.")

        user_ref = db.collection("users").document(body.user_id)
        user_ref.set({"readiness_profile": readiness_profile}, merge=True)

        print(f"✅ Readiness profile saved for user {body.user_id}")
        return result

    except Exception as e:
        print(f"❌ Error in get_readiness_score: {e}")
        raise HTTPException(status_code=500, detail=str(e))