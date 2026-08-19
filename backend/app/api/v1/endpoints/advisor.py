from fastapi import APIRouter
from app.models.schemas import DocumentAdvisorRequest, DocumentAdvisorResponse
from app.services.advisor_service import advisor_service

router = APIRouter()

@router.post("/advisory", response_model=DocumentAdvisorResponse, summary="Instant Document Advisor & Non-ECR Rules")
async def get_document_advisory(req: DocumentAdvisorRequest):
    """
    Sub-millisecond Document Advisory returning personalized document checklists,
    Non-ECR eligibility validation, and mandatory legal Annexures.
    """
    return advisor_service.get_advice(req)
