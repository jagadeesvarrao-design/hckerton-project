from typing import List
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    SlotSearchRequest,
    PSKSlotInfo,
    SlotHoldRequest,
    SlotHoldResponse
)
from app.services.slot_service import slot_service

router = APIRouter()

@router.post("/search", response_model=List[PSKSlotInfo], summary="High-Concurrency Slot Radar Search")
async def search_slots(req: SlotSearchRequest):
    """
    Search PSK and POPSK slot availability across cities and states.
    Lock-free reads designed for 100,000+ simultaneous queries.
    """
    return slot_service.search_slots(req)

@router.post("/hold", response_model=SlotHoldResponse, summary="Atomic Appointment Slot Reservation")
async def hold_slot(req: SlotHoldRequest):
    """
    Atomically hold an appointment slot for 15 minutes to eliminate race conditions
    and tatkaal checkout crashes.
    """
    try:
        return slot_service.hold_slot(req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
