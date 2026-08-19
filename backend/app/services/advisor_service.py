import json
import os
import time
from typing import Dict, Any, List
from app.models.schemas import (
    DocumentAdvisorRequest, 
    DocumentAdvisorResponse, 
    DocumentItem, 
    AnnexureItem
)
from app.core.cache import cache

class AdvisorService:
    def __init__(self):
        self.doc_data: Dict[str, Any] = {}
        self._load_rules()

    def _load_rules(self):
        file_path = os.path.join(os.path.dirname(__file__), "..", "data", "document_rules.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.doc_data = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load document_rules.json: {e}")
            self.doc_data = {"categories": {}, "annexures": {}}

    def get_advice(self, req: DocumentAdvisorRequest) -> DocumentAdvisorResponse:
        start_time = time.perf_counter()

        cache_key = f"adv_{req.service}_{req.applicant_type}_{req.scheme}_{req.has_10th_pass_certificate}_{req.is_income_tax_payer}_{req.has_name_change}_{req.is_minor_single_parent}_{req.is_lost_damaged}"
        cached = cache.get(cache_key)
        if cached:
            elapsed = (time.perf_counter() - start_time) * 1000.0
            cached_resp = DocumentAdvisorResponse(**cached)
            cached_resp.processing_latency_ms = round(elapsed, 3)
            return cached_resp

        # Determine Non-ECR Eligibility
        non_ecr = False
        non_ecr_reason = "Standard ECR (Emigration Check Required)"
        
        if req.has_10th_pass_certificate:
            non_ecr = True
            non_ecr_reason = "Eligible for Non-ECR based on 10th Standard / Matriculation or higher education certificate."
        elif req.is_income_tax_payer:
            non_ecr = True
            non_ecr_reason = "Eligible for Non-ECR based on Income Tax assessment proof."
        elif req.applicant_type == "minor":
            non_ecr = True
            non_ecr_reason = "All minors under 18 years of age are automatically entitled to Non-ECR."
        elif req.applicant_type == "senior_citizen":
            non_ecr = True
            non_ecr_reason = "Eligible for Non-ECR based on age (50+ years)."

        # Address & DOB Proof Options
        address_proofs = [
            DocumentItem(code="AADHAAR", name="Aadhaar Card / e-Aadhaar with current address", strength="HIGH", mandatory=False),
            DocumentItem(code="BANK_PASSBOOK", name="Photo Passbook of Scheduled Bank (Running account)", strength="HIGH", mandatory=False),
            DocumentItem(code="ELECTRICITY_BILL", name="Electricity Bill (Last 3 months)", strength="MEDIUM", mandatory=False),
            DocumentItem(code="RENT_AGREEMENT", name="Registered Rent Agreement (if living in rented accommodation)", strength="MEDIUM", mandatory=False)
        ]

        dob_proofs = [
            DocumentItem(code="BIRTH_CERTIFICATE", name="Birth Certificate from Municipal Authority / Registrar", strength="HIGHEST", mandatory=False),
            DocumentItem(code="TRANSFER_10TH", name="10th Class School Leaving / Matriculation Certificate", strength="HIGH", mandatory=False),
            DocumentItem(code="PAN_CARD", name="PAN Card with verified Date of Birth", strength="HIGH", mandatory=False),
            DocumentItem(code="AADHAAR_DOB", name="Aadhaar Card with full verified Date of Birth", strength="HIGH", mandatory=False)
        ]

        id_proofs = [
            DocumentItem(code="AADHAAR", name="Aadhaar Card (Original + 1 self-attested photocopy)", strength="HIGH", mandatory=True),
            DocumentItem(code="PAN_CARD", name="PAN Card (for identity & tax cross-verification)", strength="MEDIUM", mandatory=False)
        ]

        # Mandatory Annexures
        annexures = []
        guidelines = [
            "Always carry 1 set of self-attested photocopies along with original documents to the PSK.",
            "Laminated documents are discouraged if the lamination obscures watermarks or stamps."
        ]

        if req.scheme == "tatkaal":
            annexures.append(AnnexureItem(
                code="ANNEXURE_E",
                name="Annexure E (Self-Declaration of Citizenship & No Criminal Proceedings)",
                trigger="Mandatory for all Tatkaal applications",
                download_url="/api/v1/advisor/annexures/ANNEXURE_E"
            ))
            guidelines.append("Under Tatkaal scheme, verification is expedited. Ensure 3 out of 13 specified documents are ready.")

        if req.applicant_type == "minor" or req.is_minor_single_parent:
            annexures.append(AnnexureItem(
                code="ANNEXURE_D",
                name="Annexure D (Declaration for Minor Passport by Parents)",
                trigger="Mandatory for minor passport applications",
                download_url="/api/v1/advisor/annexures/ANNEXURE_D"
            ))

        if req.is_lost_damaged:
            annexures.append(AnnexureItem(
                code="ANNEXURE_F",
                name="Annexure F (Affidavit for Lost or Damaged Passport + FIR Copy)",
                trigger="Required for reissue due to lost/damaged booklet",
                download_url="/api/v1/advisor/annexures/ANNEXURE_F"
            ))
            guidelines.append("For lost passports, a police report / FIR or non-traceable certificate is mandatory.")

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        resp_dict = {
            "non_ecr_eligible": non_ecr,
            "non_ecr_reason": non_ecr_reason,
            "address_proof_options": [p.model_dump() for p in address_proofs],
            "dob_proof_options": [d.model_dump() for d in dob_proofs],
            "identity_proof_options": [i.model_dump() for i in id_proofs],
            "mandatory_annexures": [a.model_dump() for a in annexures],
            "special_guidelines": guidelines,
            "processing_latency_ms": round(elapsed_ms, 3)
        }

        cache.set(cache_key, resp_dict, ttl=86400)
        return DocumentAdvisorResponse(**resp_dict)

advisor_service = AdvisorService()
