import pytest
from app.services.police_station_service import police_station_service
from app.services.annexures_service import annexures_service
from app.services.grievance_service import grievance_service, GrievanceSubmissionRequest
from app.services.calculator_service import calculator_service
from app.services.advisor_service import advisor_service
from app.services.document_auditor import document_auditor_service
from app.services.slot_service import slot_service
from app.models.schemas import (
    FeeCalculationRequest,
    DocumentAdvisorRequest,
    DocumentAuditRequest,
    DocumentFieldExtraction,
    SlotSearchRequest,
    SlotHoldRequest
)

def test_know_your_police_station():
    # 1. Test states and districts
    states = police_station_service.list_states()
    assert "Delhi" in states
    assert "Maharashtra" in states

    districts = police_station_service.list_districts("Delhi")
    assert "New Delhi" in districts

    # 2. Test locate by district
    stations = police_station_service.locate_stations(state="Delhi", district="New Delhi")
    assert len(stations) > 0
    assert any("Tilak Marg" in s.thana_name for s in stations)

    # 3. Test locate by pincode
    pin_stations = police_station_service.locate_stations(pincode="110001")
    assert len(pin_stations) > 0
    assert pin_stations[0].state == "Delhi"

def test_annexures_catalog_and_generation():
    # 1. Test catalog list
    ann_list = annexures_service.list_all()
    assert len(ann_list) >= 10
    
    # 2. Test get by code
    ann_e = annexures_service.get_by_code("ANNEXURE_E")
    assert ann_e is not None
    assert "Tatkaal" in ann_e.purpose

    # 3. Test affidavit auto-generation
    user_data = {
        "applicant_name": "SAGAR SHARMA",
        "father_name": "SURESH SHARMA",
        "dob": "1998-05-15",
        "pob": "NEW DELHI",
        "address": "Flat 402, Green Valley, New Delhi",
        "police_station": "Tilak Marg Police Station"
    }
    gen_resp = annexures_service.generate_affidavit("ANNEXURE_E", user_data)
    assert gen_resp.is_ready_for_print is True
    assert "SAGAR SHARMA" in gen_resp.legal_text
    assert "Tilak Marg Police Station" in gen_resp.legal_text
    assert len(gen_resp.missing_fields) == 0

def test_grievance_and_helpline_service():
    # 1. Lodge Grievance
    req = GrievanceSubmissionRequest(
        file_number="DL10829384729",
        applicant_name="SAGAR SHARMA",
        contact_number="9876543210",
        email_id="sagar@example.com",
        passport_office="RPO Delhi",
        grievance_category="DELAY_IN_POLICE_VERIFICATION",
        description="Physical verification completed 5 days ago, status still pending."
    )
    rec = grievance_service.lodge_grievance(req)
    assert rec.grievance_id.startswith("GRV-MEA-")
    assert rec.status == "REGISTERED"

    # 2. Track Grievance
    tracked = grievance_service.track_grievance(rec.grievance_id)
    assert tracked is not None
    assert tracked.file_number == "DL10829384729"

    # 3. Helplines
    helplines = grievance_service.get_helplines()
    assert "1800-258-1800" in helplines["national_call_center_toll_free"]

def test_full_application_lifecycle():
    # 1. Fee Calculation
    fee_req = FeeCalculationRequest(service="fresh", scheme="tatkaal", booklet_pages=36)
    fee_resp = calculator_service.calculate_fee(fee_req)
    assert fee_resp.amount == 3500

    # 2. Document Advisory
    adv_req = DocumentAdvisorRequest(service="fresh", scheme="tatkaal", has_10th_pass_certificate=True)
    adv_resp = advisor_service.get_advice(adv_req)
    assert adv_resp.non_ecr_eligible is True

    # 3. Zero-Rejection Cross-Document Audit
    audit_req = DocumentAuditRequest(
        target_service="fresh",
        documents=[
            DocumentFieldExtraction(document_type="aadhaar", extracted_name="SAGAR SHARMA", extracted_dob="1998-05-15"),
            DocumentFieldExtraction(document_type="10th_marksheet", extracted_name="SAGAR SHARMA", extracted_dob="1998-05-15")
        ]
    )
    audit_resp = document_auditor_service.audit_documents(audit_req)
    assert audit_resp.psk_readiness_score == 100
    assert audit_resp.rejection_risk_level == "ZERO_RISK"

    # 4. Slot Search & Hold
    slots = slot_service.search_slots(SlotSearchRequest(city_or_pincode="Delhi", service_type="tatkaal"))
    assert len(slots) > 0
    hold_resp = slot_service.hold_slot(SlotHoldRequest(
        center_id=slots[0].center_id,
        appointment_date=slots[0].earliest_date,
        appointment_time="10:00 AM",
        scheme="tatkaal",
        applicant_id="APPLICANT_1001"
    ))
    assert hold_resp.hold_token.startswith("PSK-HOLD-")
