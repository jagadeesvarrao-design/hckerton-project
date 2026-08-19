import time
from typing import Dict, Any
from app.models.schemas import PassportTrackResponse, VerificationStep

class TrackerService:
    """
    Simulates and provides transparent status tracking for Passport Seva files,
    breaking down the opacity of Counter A/B/C and Police Verification.
    """
    def __init__(self):
        self._mock_records: Dict[str, Dict[str, Any]] = {
            "DL10829384729": {
                "file_number": "DL10829384729",
                "applicant_name": "SAGAR SHARMA",
                "service_type": "Fresh Passport (Normal - 36 Pages)",
                "application_date": "2026-08-16",
                "current_status": "POLICE_VERIFICATION_IN_PROGRESS",
                "estimated_delivery_date": "2026-08-28",
                "speed_post_tracking": None,
                "steps": [
                    {
                        "stage_id": "STAGE_1_APPOINTMENT",
                        "title": "PSK Visit & Token Issuance",
                        "description": "Applicant arrived at PSK Herald House, New Delhi. Token #A-42 issued.",
                        "status": "COMPLETED",
                        "timestamp": "2026-08-17 10:15 AM",
                        "officer_notes": "Queue cleared within 8 minutes."
                    },
                    {
                        "stage_id": "STAGE_2_COUNTER_A",
                        "title": "Counter A: Biometrics & Scans",
                        "description": "Digital photograph, 10-fingerprints, and original document scans completed.",
                        "status": "COMPLETED",
                        "timestamp": "2026-08-17 10:35 AM",
                        "officer_notes": "Aadhaar and 10th marksheet uploaded successfully."
                    },
                    {
                        "stage_id": "STAGE_3_COUNTER_B",
                        "title": "Counter B: Verification Officer",
                        "description": "Cross-verification of originals against MEA Central Registry.",
                        "status": "COMPLETED",
                        "timestamp": "2026-08-17 11:05 AM",
                        "officer_notes": "Non-ECR status approved."
                    },
                    {
                        "stage_id": "STAGE_4_COUNTER_C",
                        "title": "Counter C: Granting Officer",
                        "description": "Final approval and electronic passport dossier granted.",
                        "status": "COMPLETED",
                        "timestamp": "2026-08-17 11:25 AM",
                        "officer_notes": "Passport granted on Post-Police Verification basis."
                    },
                    {
                        "stage_id": "STAGE_5_POLICE",
                        "title": "Local Police Verification",
                        "description": "Dossier assigned to Tilak Marg Police Station. Officer scheduled physical visit.",
                        "status": "IN_PROGRESS",
                        "timestamp": "2026-08-18 04:00 PM",
                        "officer_notes": "Field Officer: SI R. Kumar (Mob: 9876543210). Visit scheduled between 4-6 PM."
                    },
                    {
                        "stage_id": "STAGE_6_PRINT_DISPATCH",
                        "title": "Printing & Speed Post Dispatch",
                        "description": "Security lamination, chip programming, and India Post dispatch.",
                        "status": "PENDING",
                        "timestamp": None,
                        "officer_notes": "Will initiate upon police report clearance."
                    }
                ]
            }
        }

    def track_file(self, file_number: str) -> PassportTrackResponse:
        f_clean = file_number.strip().upper()
        if f_clean in self._mock_records:
            data = self._mock_records[f_clean]
            steps = [VerificationStep(**s) for s in data["steps"]]
            return PassportTrackResponse(
                file_number=data["file_number"],
                applicant_name=data["applicant_name"],
                service_type=data["service_type"],
                application_date=data["application_date"],
                current_status=data["current_status"],
                estimated_delivery_date=data["estimated_delivery_date"],
                speed_post_tracking=data["speed_post_tracking"],
                steps=steps
            )

        # Dynamic generated tracker for any input file number
        now = time.strftime("%Y-%m-%d")
        return PassportTrackResponse(
            file_number=f_clean,
            applicant_name="VALUED CITIZEN",
            service_type="Fresh Passport (36 Pages, Normal)",
            application_date=now,
            current_status="IN_PROCESS_AT_PSK",
            estimated_delivery_date="2026-09-02",
            speed_post_tracking="EM893471029IN",
            steps=[
                VerificationStep(
                    stage_id="STAGE_1_SUBMISSION",
                    title="Online Application Submitted",
                    description="Application form received with fee clearance.",
                    status="COMPLETED",
                    timestamp=f"{now} 09:30 AM",
                    officer_notes="Payment ID: UPI_839201934"
                ),
                VerificationStep(
                    stage_id="STAGE_2_APPOINTMENT",
                    title="PSK Appointment Scheduled",
                    description="Appointment confirmed at regional Passport Seva Kendra.",
                    status="IN_PROGRESS",
                    timestamp=f"{now} 11:00 AM",
                    officer_notes="Bring original Aadhaar and 10th certificate."
                ),
                VerificationStep(
                    stage_id="STAGE_3_POLICE",
                    title="Police Verification",
                    description="Pending PSK interview clearance.",
                    status="PENDING",
                    timestamp=None,
                    officer_notes=None
                ),
                VerificationStep(
                    stage_id="STAGE_4_DISPATCH",
                    title="Speed Post Dispatch",
                    description="Pending passport printing & chip encoding.",
                    status="PENDING",
                    timestamp=None,
                    officer_notes=None
                )
            ]
        )

tracker_service = TrackerService()
