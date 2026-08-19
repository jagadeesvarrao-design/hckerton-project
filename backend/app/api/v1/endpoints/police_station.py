from typing import List, Optional
from fastapi import APIRouter, Query
from app.services.police_station_service import police_station_service, PoliceStationInfo

router = APIRouter()

@router.get("/states", response_model=List[str], summary="List all available states")
async def get_states():
    return police_station_service.list_states()

@router.get("/districts", response_model=List[str], summary="List districts in a state")
async def get_districts(state: str = Query(..., description="State name, e.g. 'Delhi', 'Maharashtra'")):
    return police_station_service.list_districts(state)

@router.get("/locate", response_model=List[PoliceStationInfo], summary="Know Your Police Station (Locate jurisdiction thana)")
async def locate_police_station(
    state: Optional[str] = Query(None, description="State"),
    district: Optional[str] = Query(None, description="District"),
    pincode: Optional[str] = Query(None, description="6-digit Pincode")
):
    """
    Sub-millisecond lookup to locate your exact police station jurisdiction
    for physical Police Verification.
    """
    return police_station_service.locate_stations(state=state, district=district, pincode=pincode)
