from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from app.services.grievance_service import grievance_service, GrievanceSubmissionRequest, GrievanceRecord

router = APIRouter()

@router.post("/lodge", response_model=GrievanceRecord, summary="Lodge Grievance or Appeal to RPO")
async def lodge_grievance(req: GrievanceSubmissionRequest):
    return grievance_service.lodge_grievance(req)

@router.get("/track/{grievance_id}", response_model=GrievanceRecord, summary="Track Grievance / Appeal Resolution Status")
async def track_grievance(grievance_id: str):
    rec = grievance_service.track_grievance(grievance_id)
    if not rec:
        raise HTTPException(status_code=404, detail=f"Grievance ID '{grievance_id}' not found.")
    return rec

@router.get("/helplines", summary="National Passport Helplines & Contact Centers")
async def get_helplines():
    return grievance_service.get_helplines()
