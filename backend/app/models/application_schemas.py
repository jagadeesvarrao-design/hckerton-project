import uuid
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

# --- User Auth Models ---
class UserRegisterRequest(BaseModel):
    passport_office: str
    given_name: str
    surname: str
    dob: str
    email_id: str
    mobile_number: str
    login_id: str
    password: str

class UserLoginRequest(BaseModel):
    login_id_or_email: str
    password_or_otp: str
    login_mode: str = "password" # "password" or "otp"

class AuthResponse(BaseModel):
    token: str
    user_name: str
    login_id: str
    passport_office: str
    status: str

# --- Official Ministry of External Affairs (MEA) Form No. 1 Complete Data Model ---
class FreshPassportSubmission(BaseModel):
    # SECTION 1: Service Required
    applying_for: str = "Fresh Passport" # "Fresh Passport"
    type_of_application: str = "Normal" # "Normal" or "Tatkaal"
    type_of_passport_booklet: str = "36 Pages" # "36 Pages" or "60 Pages"
    validity_required: str = "10 Years" # "10 Years" or "5 Years (for minors)"
    
    # SECTION 2: Applicant Personal Details
    given_name: str
    surname: Optional[str] = ""
    aliases_known: bool = False
    alias_given_name: Optional[str] = None
    alias_surname: Optional[str] = None
    name_changed: bool = False
    previous_given_name: Optional[str] = None
    previous_surname: Optional[str] = None
    dob: str
    place_of_birth: str
    district: str
    state: str
    country_of_birth: str = "India"
    gender: str = "Male" # "Male", "Female", "Transgender"
    marital_status: str = "Single" # "Single", "Married", "Divorced", "Widow/Widower", "Separated"
    citizenship_by: str = "Birth" # "Birth", "Descent", "Registration/Naturalization"
    employment_type: str = "Private" # "Govt/PSU", "Private", "Self Employed", "Student", "Homemaker", "Retired", "Others"
    is_parent_or_spouse_govt_servant: bool = False
    educational_qualification: str = "10th Pass & Above" # "7th or less", "Between 8th and 9th", "10th Pass & Above", "Graduate & Above"
    visible_distinguishing_mark: Optional[str] = None
    
    # SECTION 3: Family Details
    father_given_name: str
    father_surname: Optional[str] = ""
    mother_given_name: str
    mother_surname: Optional[str] = ""
    legal_guardian_given_name: Optional[str] = None
    legal_guardian_surname: Optional[str] = None
    spouse_given_name: Optional[str] = None
    spouse_surname: Optional[str] = None
    
    # SECTION 4: Present Residential Address & Police Station
    is_present_address_out_of_india: bool = False
    present_address_street: str
    present_city: str
    present_district: str
    present_police_station: str
    present_state: str = "Delhi"
    present_pincode: str
    mobile_number: str
    telephone_number: Optional[str] = None
    email_id: str
    is_permanent_address_same: bool = True
    permanent_address_street: Optional[str] = None
    
    # SECTION 5: Emergency Contact Details
    emergency_contact_name: str
    emergency_contact_address: str
    emergency_contact_mobile: str
    emergency_contact_email: Optional[str] = None

    # SECTION 6: Official MEA Document Information (Proof of Address & DOB)
    poa_document_type: str = "Aadhaar Card (UIDAI)"
    poa_document_number: str
    poa_issuing_authority: Optional[str] = "UIDAI / Govt of India"
    poa_issue_date: Optional[str] = None
    
    dob_document_type: str = "Matriculation / 10th Standard Passing Certificate"
    dob_document_number: str
    dob_issuing_authority: Optional[str] = "CBSE / State Board"
    dob_issue_date: Optional[str] = None
    
    is_non_ecr_eligible: bool = True
    non_ecr_category: str = "Matriculation (10th Standard) and Above"
    non_ecr_proof_document: str = "10th Standard Marksheet & Passing Certificate"
    non_ecr_proof_number: Optional[str] = None
    
    aadhaar_number: Optional[str] = None
    pan_number: Optional[str] = None
    voter_id_number: Optional[str] = None
    driving_license_number: Optional[str] = None
    
    # SECTION 7: Previous Passport / Application Declarations
    have_held_identity_certificate: bool = False
    have_applied_before: bool = False
    previous_application_file_no: Optional[str] = None
    previous_passport_office: Optional[str] = None

    # SECTION 8: Statutory Legal & Criminal Clearance Declarations (Passports Act 1967)
    criminal_proceedings_pending: bool = False
    warrant_or_summons_issued: bool = False
    convicted_by_court: bool = False
    passport_refused_or_denied_earlier: bool = False
    granted_political_asylum_abroad: bool = False
    returned_on_emergency_certificate: bool = False
    
    # SECTION 9: Self-Declaration Agreement
    self_declaration_accepted: bool = True

class FreshSubmissionResponse(BaseModel):
    arn_number: str
    applicant_name: str
    service_type: str
    submission_date: str
    fee_amount: int
    non_ecr_status: bool
    status: str
    receipt_url: str
    verified_documents_summary: Dict[str, Any]
    statutory_clearances_passed: bool

# --- Existing User / Re-issue & Lost Passport Models ---
class ExistingUserLookupRequest(BaseModel):
    old_passport_number: str
    dob: str
    expiry_date: Optional[str] = None

class ExistingUserServiceRequest(BaseModel):
    service_category: str # "RENEWAL_EXPIRED", "LOST_DAMAGED", "CHANGE_PARTICULARS", "PCC"
    old_passport_number: str
    applicant_name: str
    dob: str
    reason_description: str
    
    # For Lost/Damaged
    fir_number: Optional[str] = None
    fir_date: Optional[str] = None
    police_station: Optional[str] = None
    loss_circumstances: Optional[str] = None
    
    # For Particulars Change
    field_to_change: Optional[str] = None
    new_value: Optional[str] = None
    supporting_doc_type: Optional[str] = None

class ExistingUserActionResponse(BaseModel):
    service_ref_no: str
    service_name: str
    old_passport_number: str
    generated_annexure_code: Optional[str] = None
    generated_annexure_text: Optional[str] = None
    action_status: str
    fee_payable: int
    next_steps: List[str]
