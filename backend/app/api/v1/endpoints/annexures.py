from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Body
from app.services.annexures_service import annexures_service, AnnexureDetail, GeneratedAnnexureResponse

router = APIRouter()

@router.get("/catalog", response_model=List[AnnexureDetail], summary="List all official MEA Annexures (A to M)")
async def get_annexures_catalog(category: Optional[str] = Query(None, description="Filter by category")):
    return annexures_service.list_all(category)

@router.get("/{code}", response_model=AnnexureDetail, summary="Get details of a specific Annexure")
async def get_annexure_by_code(code: str):
    ann = annexures_service.get_by_code(code)
    if not ann:
        raise HTTPException(status_code=404, detail=f"Annexure '{code}' not found.")
    return ann

@router.post("/{code}/generate", response_model=GeneratedAnnexureResponse, summary="Auto-Generate legal affidavit with user data")
async def generate_annexure_affidavit(code: str, user_data: Dict[str, Any] = Body(...)):
    try:
        return annexures_service.generate_affidavit(code, user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
