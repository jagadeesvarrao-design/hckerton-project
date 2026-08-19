from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --- Fee Calculator Schemas ---
class FeeCalculationRequest(BaseModel):
    service: str = Field(..., description="Service type: 'fresh', 'reissue', 'pcc', 'surrender'")
    applicant_age_group: str = Field("adult", description="'adult', 'minor_under_15', 'minor_15_to_18'")
    booklet_pages: int = Field(36, description="36 or 60 pages")
    scheme: str = Field("normal", description="'normal' or 'tatkaal'")
    validity_years: int = Field(10, description="5 or 10 years")
    reason: Optional[str] = Field(None, description="For reissue: 'validity_expired', 'exhaustion_of_pages', 'lost_damaged', 'change_in_personal_particulars'")

class FeeCalculationResponse(BaseModel):
    service: str
    scheme: str
    amount: int
    currency: str = "INR"
    description: str
    tatkaal_surcharge: int = 0
    calculation_latency_ms: float

# --- Document Advisor Schemas ---
class DocumentAdvisorRequest(BaseModel):
    service: str = Field("fresh", description="fresh, reissue, pcc")
    applicant_type: str = Field("adult", description="adult, minor, senior_citizen, govt_servant")
    scheme: str = Field("normal", description="normal or tatkaal")
    has_10th_pass_certificate: bool = True
    is_income_tax_payer: bool = False
    has_name_change: bool = False
    is_minor_single_parent: bool = False
    is_lost_damaged: bool = False

class DocumentItem(BaseModel):
    code: str
    name: str
    strength: str
    mandatory: bool = False

class AnnexureItem(BaseModel):
    code: str
    name: str
    trigger: str
    download_url: Optional[str] = None

class DocumentAdvisorResponse(BaseModel):
    non_ecr_eligible: bool
    non_ecr_reason: str
    address_proof_options: List[DocumentItem]
    dob_proof_options: List[DocumentItem]
    identity_proof_options: List[DocumentItem]
    mandatory_annexures: List[AnnexureItem]
    special_guidelines: List[str]
    processing_latency_ms: float

# --- Document Auditor & Pre-fill Schemas ---
class DocumentFieldExtraction(BaseModel):
    document_type: str # 'aadhaar', '10th_marksheet', 'pan', 'utility_bill', 'voter_id'
    extracted_name: Optional[str] = None
    extracted_dob: Optional[str] = None
    extracted_father_name: Optional[str] = None
    extracted_gender: Optional[str] = None
    extracted_address: Optional[str] = None
    extracted_pincode: Optional[str] = None
    id_number_masked: Optional[str] = None
    confidence_score: float = 1.0

class DiscrepancyItem(BaseModel):
    field: str
    severity: str # 'CRITICAL', 'WARNING', 'INFO'
    doc1_type: str
    doc1_value: str
    doc2_type: str
    doc2_value: str
    explanation: str
    suggested_fix: str
    required_annexure: Optional[str] = None

class DocumentAuditRequest(BaseModel):
    target_service: str = "fresh"
    documents: List[DocumentFieldExtraction]

class AutoFilledPassportForm(BaseModel):
    given_name: str
    surname: str
    date_of_birth: str
    gender: str
    place_of_birth: str
    district: str
    state: str
    father_given_name: str
    father_surname: str
    mother_given_name: str
    mother_surname: str
    present_address: str
    pincode: str
    mobile_number: Optional[str] = None
    email_id: Optional[str] = None
    is_non_ecr: bool = True
    annexures_attached: List[str] = []

class DocumentAuditResponse(BaseModel):
    psk_readiness_score: int # 0 to 100
    rejection_risk_level: str # 'ZERO_RISK', 'LOW_RISK', 'HIGH_RISK_REJECTION'
    discrepancies: List[DiscrepancyItem]
    non_ecr_status: bool
    non_ecr_evidence: str
    recommended_annexures: List[str]
    auto_filled_form: AutoFilledPassportForm
    audit_summary: str
    latency_ms: float

# --- Slot Radar Schemas ---
class SlotSearchRequest(BaseModel):
    city_or_pincode: Optional[str] = None
    state: Optional[str] = None
    service_type: str = "normal" # 'normal' or 'tatkaal'

class PSKSlotInfo(BaseModel):
    center_id: str
    center_name: str
    center_type: str
    city: str
    state: str
    address: str
    available_slots: int
    earliest_date: str
    booking_status: str # 'AVAILABLE', 'FAST_FILLING', 'SOLD_OUT'
    distance_km: Optional[float] = None

class SlotHoldRequest(BaseModel):
    center_id: str
    appointment_date: str
    appointment_time: str
    scheme: str = "normal"
    applicant_id: str

class SlotHoldResponse(BaseModel):
    hold_token: str
    center_name: str
    appointment_datetime: str
    expires_in_seconds: int
    amount_payable: int
    status: str

# --- Multilingual Citizen Copilot Schemas ---
class CopilotChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = []
    language: str = "en" # 'en', 'hi', 'te', 'ta', 'mr', 'bn', 'kn'

class CopilotChatResponse(BaseModel):
    reply: str
    intent_detected: str
    suggested_actions: List[Dict[str, str]]
    audio_tts_available: bool = False

# --- Live Tracker Schemas ---
class PassportTrackRequest(BaseModel):
    file_number: str

class VerificationStep(BaseModel):
    stage_id: str
    title: str
    description: str
    status: str # 'COMPLETED', 'IN_PROGRESS', 'PENDING'
    timestamp: Optional[str] = None
    officer_notes: Optional[str] = None

class PassportTrackResponse(BaseModel):
    file_number: str
    applicant_name: str
    service_type: str
    application_date: str
    current_status: str
    estimated_delivery_date: str
    speed_post_tracking: Optional[str] = None
    steps: List[VerificationStep]
