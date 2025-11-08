from fastapi import APIRouter
from Backend.api.v1.schemas.readiness_models import ReadinessForm, ReadinessResponse
from Backend.api.v1.services.readiness_service import compute_readiness

router = APIRouter()

@router.post("", response_model=ReadinessResponse)
async def get_readiness_score(body: ReadinessForm):
    """
    POST /api/v1/readiness
    Receives user's financial info and returns readiness metrics.
    """
    return compute_readiness(body)
