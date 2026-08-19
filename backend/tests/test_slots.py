import pytest
from app.services.slot_service import slot_service
from app.models.schemas import SlotSearchRequest, SlotHoldRequest

def test_slot_search_and_hold():
    # Search slots in Delhi
    search_req = SlotSearchRequest(city_or_pincode="Delhi", service_type="normal")
    slots = slot_service.search_slots(search_req)
    assert len(slots) > 0
    
    first_slot = slots[0]
    initial_avail = first_slot.available_slots
    assert initial_avail > 0

    # Hold a slot atomically
    hold_req = SlotHoldRequest(
        center_id=first_slot.center_id,
        appointment_date=first_slot.earliest_date,
        appointment_time="10:30 AM",
        scheme="normal",
        applicant_id="APPLICANT_USER_99"
    )
    hold_resp = slot_service.hold_slot(hold_req)
    assert hold_resp.hold_token.startswith("PSK-HOLD-")
    assert hold_resp.expires_in_seconds == 900
    assert hold_resp.amount_payable == 1500

    # Verify inventory was decremented atomically
    slots_after = slot_service.search_slots(search_req)
    updated_slot = next(s for s in slots_after if s.center_id == first_slot.center_id)
    assert updated_slot.available_slots == initial_avail - 1
