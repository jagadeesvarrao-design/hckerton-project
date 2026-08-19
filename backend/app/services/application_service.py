import uuid
import time
import re
from typing import Dict, Any, List, Optional
from app.models.application_schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    AuthResponse,
    FreshPassportSubmission,
    FreshSubmissionResponse,
    ExistingUserLookupRequest,
    ExistingUserServiceRequest,
    ExistingUserActionResponse
)

class ApplicationService:
    def __init__(self):
        self._existing_passports: Dict[str, Dict[str, Any]] = {
            "Z1234567": {
                "passport_number": "Z1234567",
                "applicant_name": "SAGAR SHARMA",
                "dob": "1998-05-15",
                "place_of_birth": "NEW DELHI",
                "issue_date": "2016-08-20",
                "expiry_date": "2026-08-19",
                "place_of_issue": "RPO DELHI",
                "status": "VALID",
                "ecr_status": "Non-ECR"
            },
            "P9876543": {
                "passport_number": "P9876543",
                "applicant_name": "LAKSHMI DURGA",
                "dob": "1995-10-12",
                "place_of_birth": "VISAKHAPATNAM",
                "issue_date": "2014-03-10",
                "expiry_date": "2024-03-09",
                "place_of_issue": "RPO VISAKHAPATNAM",
                "status": "EXPIRED",
                "ecr_status": "Non-ECR"
            }
        }

    def register_user(self, req: UserRegisterRequest) -> AuthResponse:
        token = f"TOKEN-MEA-{uuid.uuid4().hex[:12].upper()}"
        return AuthResponse(
            token=token,
            user_name=f"{req.given_name} {req.surname}".strip(),
            login_id=req.login_id,
            passport_office=req.passport_office,
            status="REGISTERED_SUCCESS"
        )

    def login_user(self, req: UserLoginRequest) -> AuthResponse:
        token = f"TOKEN-MEA-{uuid.uuid4().hex[:12].upper()}"
        name = "SAGAR SHARMA" if "sagar" in req.login_id_or_email.lower() else "AUTHENTICATED CITIZEN"
        return AuthResponse(
            token=token,
            user_name=name,
            login_id=req.login_id_or_email,
            passport_office="RPO Delhi",
            status="LOGIN_SUCCESS"
        )

    def submit_fresh_application(self, req: FreshPassportSubmission) -> FreshSubmissionResponse:
        arn = f"ARN-MEA-{time.strftime('%y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        now_date = time.strftime("%Y-%m-%d")
        
        # Determine Fee
        fee = 3500 if req.type_of_application.lower() == "tatkaal" else 1500
        if req.type_of_passport_booklet == "60 Pages":
            fee += 500

        full_name = f"{req.given_name} {req.surname}".strip()

        doc_summary = {
            "proof_of_address": {
                "document": req.poa_document_type,
                "document_number": req.poa_document_number,
                "issuing_authority": req.poa_issuing_authority or "UIDAI / Competent Authority",
                "issue_date": req.poa_issue_date or "N/A"
            },
            "proof_of_dob": {
                "document": req.dob_document_type,
                "document_number": req.dob_document_number,
                "issuing_authority": req.dob_issuing_authority or "Recognized Board / Municipal Authority",
                "issue_date": req.dob_issue_date or "N/A"
            },
            "non_ecr_status": {
                "eligible": req.is_non_ecr_eligible,
                "category": req.non_ecr_category,
                "supporting_proof": req.non_ecr_proof_document,
                "proof_number": req.non_ecr_proof_number or req.dob_document_number
            },
            "national_id_proofs": {
                "aadhaar": req.aadhaar_number or "Provided",
                "pan": req.pan_number or "N/A",
                "voter_id": req.voter_id_number or "N/A",
                "driving_license": req.driving_license_number or "N/A"
            },
            "statutory_declarations": {
                "criminal_proceedings_pending": req.criminal_proceedings_pending,
                "warrant_or_summons_issued": req.warrant_or_summons_issued,
                "convicted_by_court": req.convicted_by_court,
                "passport_refused_or_denied_earlier": req.passport_refused_or_denied_earlier,
                "granted_political_asylum_abroad": req.granted_political_asylum_abroad,
                "returned_on_emergency_certificate": req.returned_on_emergency_certificate
            }
        }

        clearances_ok = not any([
            req.criminal_proceedings_pending,
            req.warrant_or_summons_issued,
            req.convicted_by_court,
            req.passport_refused_or_denied_earlier,
            req.granted_political_asylum_abroad,
            req.returned_on_emergency_certificate
        ])

        return FreshSubmissionResponse(
            arn_number=arn,
            applicant_name=full_name,
            service_type=f"Fresh Passport ({req.type_of_application} - {req.type_of_passport_booklet})",
            submission_date=now_date,
            fee_amount=fee,
            non_ecr_status=req.is_non_ecr_eligible,
            status="APPLICATION_SUBMITTED_SUCCESS",
            receipt_url=f"/api/v1/application/receipt/{arn}",
            verified_documents_summary=doc_summary,
            statutory_clearances_passed=clearances_ok
        )

    def lookup_existing_passport(self, req: ExistingUserLookupRequest) -> Dict[str, Any]:
        p_clean = req.old_passport_number.strip().upper()
        if p_clean in self._existing_passports:
            return {
                "found": True,
                "data": self._existing_passports[p_clean],
                "message": "Passport record located in MEA central registry."
            }
        
        if re.match(r'^[A-Z][0-9]{7}$', p_clean):
            mock_data = {
                "passport_number": p_clean,
                "applicant_name": "VALUED CITIZEN",
                "dob": req.dob,
                "place_of_birth": "INDIA",
                "issue_date": "2018-05-10",
                "expiry_date": req.expiry_date or "2028-05-09",
                "place_of_issue": "RPO REGIONAL",
                "status": "VALID",
                "ecr_status": "Non-ECR"
            }
            return {
                "found": True,
                "data": mock_data,
                "message": "Record retrieved successfully."
            }

        return {
            "found": False,
            "data": None,
            "message": "Passport number not found. Ensure format is 1 letter followed by 7 digits (e.g. Z1234567)."
        }

    def process_existing_user_service(self, req: ExistingUserServiceRequest) -> ExistingUserActionResponse:
        ref_no = f"SRV-MEA-{uuid.uuid4().hex[:8].upper()}"
        ann_code = None
        ann_text = None
        
        if req.service_category == "LOST_DAMAGED":
            ann_code = "ANNEXURE_F"
            ann_text = f"I, {req.applicant_name}, declare that my passport {req.old_passport_number} was lost/damaged under circumstances: {req.loss_circumstances or 'Accidental loss during transit'}. A police report was lodged at {req.police_station or 'Local Police Station'} under FIR #{req.fir_number or 'FIR/2026/9021'} dated {req.fir_date or time.strftime('%Y-%m-%d')}."
            fee = 3000
            service_title = "Replacement of Lost/Damaged Passport"
            next_steps = [
                "1. Carry original copy of Police FIR / Non-Traceable Certificate.",
                "2. Print and notarize the auto-generated Annexure 'F' affidavit below.",
                "3. Attend your scheduled appointment at PSK for biometric recapture."
            ]
        elif req.service_category == "RENEWAL_EXPIRED":
            fee = 1500
            service_title = "Re-issue / Renewal of Expired Passport"
            next_steps = [
                "1. Carry previous original passport book for cancellation.",
                "2. Carry 1 self-attested photocopy of first and last two pages of old passport.",
                "3. No fresh police verification required if address is unchanged."
            ]
        elif req.service_category == "CHANGE_PARTICULARS":
            fee = 1500
            service_title = f"Change in Particulars ({req.field_to_change or 'Personal Details'})"
            ann_code = "ANNEXURE_E"
            ann_text = f"I, {req.applicant_name}, holder of passport {req.old_passport_number}, hereby affirm that my updated {req.field_to_change or 'particulars'} is {req.new_value or 'N/A'}, supported by valid government identity proof."
            next_steps = [
                f"1. Carry supporting proof for {req.field_to_change or 'update'}.",
                "2. Carry old original passport book for cancellation.",
                "3. Verified endorsement will be printed on the new passport booklet."
            ]
        else:
            fee = 500
            service_title = "Police Clearance Certificate (PCC)"
            next_steps = [
                "1. Carry old valid passport in original.",
                "2. Carry proof of employment / visa requirement.",
                "3. PCC will be issued upon clearance from local police district."
            ]

        return ExistingUserActionResponse(
            service_ref_no=ref_no,
            service_name=service_title,
            old_passport_number=req.old_passport_number,
            generated_annexure_code=ann_code,
            generated_annexure_text=ann_text,
            action_status="SERVICE_REQUEST_PROCESSED_SUCCESS",
            fee_payable=fee,
            next_steps=next_steps
        )

application_service = ApplicationService()
