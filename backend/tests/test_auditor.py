import pytest
from app.services.document_auditor import document_auditor_service
from app.models.schemas import DocumentAuditRequest, DocumentFieldExtraction

def test_zero_discrepancy_audit():
    req = DocumentAuditRequest(
        target_service="fresh",
        documents=[
            DocumentFieldExtraction(
                document_type="aadhaar",
                extracted_name="SAGAR SHARMA",
                extracted_dob="1998-05-15",
                extracted_father_name="SURESH SHARMA",
                extracted_gender="Male",
                extracted_address="Flat 402, Green Valley, Outer Ring Road, New Delhi",
                extracted_pincode="110002"
            ),
            DocumentFieldExtraction(
                document_type="10th_marksheet",
                extracted_name="SAGAR SHARMA",
                extracted_dob="1998-05-15",
                extracted_father_name="SURESH SHARMA"
            )
        ]
    )
    
    resp = document_auditor_service.audit_documents(req)
    assert resp.psk_readiness_score == 100
    assert resp.rejection_risk_level == "ZERO_RISK"
    assert resp.non_ecr_status is True
    assert resp.auto_filled_form.given_name == "SAGAR"
    assert resp.auto_filled_form.surname == "SHARMA"
    assert resp.auto_filled_form.is_non_ecr is True

def test_initial_expansion_discrepancy_detection():
    req = DocumentAuditRequest(
        target_service="fresh",
        documents=[
            DocumentFieldExtraction(
                document_type="aadhaar",
                extracted_name="S. SHARMA",
                extracted_dob="1998-05-15",
                extracted_father_name="SURESH SHARMA"
            ),
            DocumentFieldExtraction(
                document_type="10th_marksheet",
                extracted_name="SAGAR SHARMA",
                extracted_dob="1998-05-15",
                extracted_father_name="SURESH SHARMA"
            )
        ]
    )
    
    resp = document_auditor_service.audit_documents(req)
    assert resp.psk_readiness_score >= 80
    assert resp.rejection_risk_level == "LOW_RISK"
    assert len(resp.discrepancies) == 1
    assert resp.discrepancies[0].severity == "WARNING"
    assert "initial" in resp.discrepancies[0].explanation.lower()
