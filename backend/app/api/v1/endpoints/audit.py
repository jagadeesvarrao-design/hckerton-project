from fastapi import APIRouter
from app.models.schemas import DocumentAuditRequest, DocumentAuditResponse
from app.services.document_auditor import document_auditor_service

router = APIRouter()

@router.post("/verify", response_model=DocumentAuditResponse, summary="Zero-Rejection Cross-Document Audit & Auto-Fill")
async def verify_documents(req: DocumentAuditRequest):
    """
    Performs deep cross-document entity alignment (name spelling, DOB matching, father's name,
    Non-ECR calculation, Annexure determination) and auto-populates the official Passport Form.
    """
    return document_auditor_service.audit_documents(req)
