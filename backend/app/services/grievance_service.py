import uuid
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class GrievanceSubmissionRequest(BaseModel):
    file_number: str
    applicant_name: str
    contact_number: str
    email_id: str
    passport_office: str
    grievance_category: str # 'DELAY_IN_POLICE_VERIFICATION', 'PAYMENT_FAILURE', 'APPOINTMENT_RESCHEDULING', 'REJECTION_CLARIFICATION', 'DISPATCH_DELAY'
    description: str

class GrievanceRecord(BaseModel):
    grievance_id: str
    file_number: str
    applicant_name: str
    passport_office: str
    category: str
    status: str # 'REGISTERED', 'ASSIGNED_TO_RPO', 'IN_INVESTIGATION', 'RESOLVED'
    assigned_officer: str
    created_at: str
    expected_resolution_date: str
    remarks: str

class GrievanceService:
    def __init__(self):
        self._records: Dict[str, Dict[str, Any]] = {
            "GRV-MEA-882910": {
                "grievance_id": "GRV-MEA-882910",
                "file_number": "DL10829384729",
                "applicant_name": "SAGAR SHARMA",
                "passport_office": "RPO Delhi",
                "category": "DELAY_IN_POLICE_VERIFICATION",
                "status": "ASSIGNED_TO_RPO",
                "assigned_officer": "Dy. Passport Officer (Public Relations)",
                "created_at": "2026-08-18",
                "expected_resolution_date": "2026-08-22",
                "remarks": "Notice issued to District SP Office to expedite field verification."
            }
        }

    def lodge_grievance(self, req: GrievanceSubmissionRequest) -> GrievanceRecord:
        gid = f"GRV-MEA-{uuid.uuid4().hex[:6].upper()}"
        now_date = time.strftime("%Y-%m-%d")
        exp_date = time.strftime("%Y-%m-%d", time.localtime(time.time() + 4 * 86400)) # 4 days SLA

        rec = {
            "grievance_id": gid,
            "file_number": req.file_number.strip().upper(),
            "applicant_name": req.applicant_name.strip(),
            "passport_office": req.passport_office,
            "category": req.grievance_category,
            "status": "REGISTERED",
            "assigned_officer": f"Public Grievance Cell ({req.passport_office})",
            "created_at": now_date,
            "expected_resolution_date": exp_date,
            "remarks": "Grievance acknowledged. Assigned to regional nodal officer for priority resolution within 48 hours."
        }
        self._records[gid] = rec
        return GrievanceRecord(**rec)

    def track_grievance(self, grievance_id: str) -> Optional[GrievanceRecord]:
        g_clean = grievance_id.strip().upper()
        rec = self._records.get(g_clean)
        return GrievanceRecord(**rec) if rec else None

    def get_helplines(self) -> Dict[str, Any]:
        return {
            "national_call_center_toll_free": "1800-258-1800",
            "operating_hours": "8:00 AM to 10:00 PM (Monday to Saturday)",
            "email_support": "support@passportindia.gov.in",
            "sms_service": "Send 'STATUS <File Number>' to 9704100100",
            "emergency_consular_services": "+91-11-2338-7000",
            "cpgrams_portal_url": "https://pgportal.gov.in/"
        }

grievance_service = GrievanceService()
