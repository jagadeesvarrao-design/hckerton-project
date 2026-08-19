from fastapi import APIRouter
from app.models.schemas import FeeCalculationRequest, FeeCalculationResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/calculate", response_model=FeeCalculationResponse, summary="Instant Passport Fee Calculation (<1ms)")
async def calculate_fee(req: FeeCalculationRequest):
    """
    Sub-millisecond fee calculator supporting all Passport categories:
    Fresh, Re-issue, Tatkaal, Jumbo (60 pages), Minors, PCC, and Surrender.
    """
    return calculator_service.calculate_fee(req)
