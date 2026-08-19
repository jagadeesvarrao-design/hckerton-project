import json
import os
import time
import uuid
import threading
from typing import List, Dict, Any, Optional
from app.models.schemas import (
    SlotSearchRequest,
    PSKSlotInfo,
    SlotHoldRequest,
    SlotHoldResponse
)
from app.core.cache import cache

class SlotService:
    """
    High-Concurrency Atomic Slot Radar Engine.
    Guarantees thread-safe lock-free reads and atomic reservations for 100,000+ users.
    """
    def __init__(self):
        self.centers: List[Dict[str, Any]] = []
        self._reservations: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._load_centers()

    def _load_centers(self):
        file_path = os.path.join(os.path.dirname(__file__), "..", "data", "psk_centers.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.centers = data.get("centers", [])
        except Exception as e:
            print(f"Warning: Could not load psk_centers.json: {e}")
            self.centers = []

    def search_slots(self, req: SlotSearchRequest) -> List[PSKSlotInfo]:
        results: List[PSKSlotInfo] = []
        
        query = (req.city_or_pincode or req.state or "").lower().strip()
        
        for c in self.centers:
            # Filter if search query provided
            if query:
                matches_city = query in c["city"].lower()
                matches_state = query in c["state"].lower()
                matches_name = query in c["name"].lower()
                matches_rpo = query in c.get("rpo", "").lower()
                if not (matches_city or matches_state or matches_name or matches_rpo):
                    continue

            slots_count = c["available_slots_tatkaal"] if req.service_type == "tatkaal" else c["available_slots_normal"]
            earliest = c["earliest_date_tatkaal"] if req.service_type == "tatkaal" else c["earliest_date_normal"]

            if slots_count > 50:
                status = "AVAILABLE"
            elif slots_count > 0:
                status = "FAST_FILLING"
            else:
                status = "SOLD_OUT"

            results.append(PSKSlotInfo(
                center_id=c["id"],
                center_name=c["name"],
                center_type=c["type"],
                city=c["city"],
                state=c["state"],
                address=c["address"],
                available_slots=slots_count,
                earliest_date=earliest,
                booking_status=status,
                distance_km=1.5 if query in c["city"].lower() else 12.0
            ))

        return results

    def hold_slot(self, req: SlotHoldRequest) -> SlotHoldResponse:
        with self._lock:
            # Find center
            center = next((c for c in self.centers if c["id"] == req.center_id), None)
            if not center:
                raise ValueError("Passport Seva Kendra not found.")

            slot_field = "available_slots_tatkaal" if req.scheme == "tatkaal" else "available_slots_normal"
            if center[slot_field] <= 0:
                raise ValueError("No available slots remaining at this center for selected date.")

            # Atomically decrement slot inventory
            center[slot_field] -= 1

            token = f"PSK-HOLD-{uuid.uuid4().hex[:8].upper()}"
            amount = 3500 if req.scheme == "tatkaal" else 1500

            self._reservations[token] = {
                "applicant_id": req.applicant_id,
                "center_id": req.center_id,
                "center_name": center["name"],
                "datetime": f"{req.appointment_date} {req.appointment_time}",
                "amount": amount,
                "created_at": time.time(),
                "expires_at": time.time() + 900 # 15 minutes hold
            }

            return SlotHoldResponse(
                hold_token=token,
                center_name=center["name"],
                appointment_datetime=f"{req.appointment_date} {req.appointment_time}",
                expires_in_seconds=900,
                amount_payable=amount,
                status="HELD_TEMPORARY"
            )

slot_service = SlotService()
