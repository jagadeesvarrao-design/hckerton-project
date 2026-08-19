from typing import Dict, Any
from fastapi import APIRouter, HTTPException
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
from app.services.application_service import application_service

router = APIRouter()

@router.post("/auth/register", response_model=AuthResponse, summary="Citizen Account Registration")
async def register(req: UserRegisterRequest):
    return application_service.register_user(req)

@router.post("/auth/login", response_model=AuthResponse, summary="Citizen Login (Password or Instant OTP)")
async def login(req: UserLoginRequest):
    return application_service.login_user(req)

@router.post("/fresh/submit", response_model=FreshSubmissionResponse, summary="Submit Fresh Passport Application (Path 1 - New Users)")
async def submit_fresh(req: FreshPassportSubmission):
    """
    Submits a full fresh passport application form and generates an official Application Reference Number (ARN).
    """
    return application_service.submit_fresh_application(req)

@router.post("/existing/lookup", summary="Lookup Existing Passport Record by Passport Number (Path 2 - Old Users)")
async def lookup_existing(req: ExistingUserLookupRequest):
    """
    Validates and fetches existing passport records for renewal, lost reports, or particulars changes.
    """
    res = application_service.lookup_existing_passport(req)
    if not res["found"]:
        raise HTTPException(status_code=404, detail=res["message"])
    return res

@router.post("/existing/service-request", response_model=ExistingUserActionResponse, summary="Process Existing User Re-issue / Lost Report / Particulars Change")
async def process_service_request(req: ExistingUserServiceRequest):
    return application_service.process_existing_user_service(req)
