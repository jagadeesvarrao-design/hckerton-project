from fastapi import APIRouter
from app.models.schemas import PassportTrackRequest, PassportTrackResponse
from app.services.tracker_service import tracker_service

router = APIRouter()

@router.post("/track", response_model=PassportTrackResponse, summary="Live PSK Counter & Police Verification Tracker")
async def track_passport(req: PassportTrackRequest):
    """
    Transparent visual timeline tracking Counter A, Counter B, Counter C,
    assigned Thana police officer, and Speed Post tracking.
    """
    return tracker_service.track_file(req.file_number)
