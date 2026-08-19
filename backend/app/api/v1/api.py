from fastapi import APIRouter
from app.api.v1.endpoints import (
    calculator,
    advisor,
    slots,
    audit,
    copilot,
    tracker,
    police_station,
    annexures,
    grievance,
    application
)

api_router = APIRouter()

api_router.include_router(application.router, prefix="/application", tags=["Citizen Onboarding & Pathways"])
api_router.include_router(calculator.router, prefix="/calculator", tags=["Fee Calculator"])
api_router.include_router(advisor.router, prefix="/advisor", tags=["Document Advisor"])
api_router.include_router(slots.router, prefix="/slots", tags=["Slot Radar & Booking"])
api_router.include_router(audit.router, prefix="/audit", tags=["Zero-Rejection Auditor"])
api_router.include_router(copilot.router, prefix="/copilot", tags=["Citizen Copilot"])
api_router.include_router(tracker.router, prefix="/tracker", tags=["Application Tracker"])
api_router.include_router(police_station.router, prefix="/police-station", tags=["Know Your Police Station"])
api_router.include_router(annexures.router, prefix="/annexures", tags=["Forms & Legal Annexures"])
api_router.include_router(grievance.router, prefix="/grievance", tags=["Grievance & Helplines"])
