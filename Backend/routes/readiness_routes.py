from fastapi import APIRouter
from Backend.schemas.readiness_model import ReadinessForm, ReadinessResponse
from Backend.services.readiness_service import compute_readiness

router = APIRouter(prefix="/readiness", tags=["readiness"])

@router.post("/", response_model=ReadinessResponse)
async def get_readiness_score(body: ReadinessForm):
    """
    POST /api/v1/readiness
    Receives user's financial info and returns readiness metrics.
    """
    return compute_readiness(body)
