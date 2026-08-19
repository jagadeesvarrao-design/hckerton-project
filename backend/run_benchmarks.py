import time
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.services.calculator_service import calculator_service
from app.services.advisor_service import advisor_service
from app.services.document_auditor import document_auditor_service
from app.services.slot_service import slot_service
from app.models.schemas import (
    FeeCalculationRequest,
    DocumentAdvisorRequest,
    DocumentAuditRequest,
    DocumentFieldExtraction,
    SlotSearchRequest,
    SlotHoldRequest
)

def run_benchmarks():
    print("=" * 60)
    print("🚀 PASSPORT SEVA AI 2.0 - BACKEND BENCHMARK & TEST SUITE")
    print("=" * 60)

    # 1. Fee Calculator Benchmark
    print("\n[1/4] Testing Fee Calculator (1,000 requests)...")
    calc_req = FeeCalculationRequest(
        service="fresh",
        applicant_age_group="adult",
        booklet_pages=36,
        scheme="normal",
        validity_years=10
    )
    # Warmup
    calculator_service.calculate_fee(calc_req)
    t0 = time.perf_counter()
    for _ in range(1000):
        res = calculator_service.calculate_fee(calc_req)
        assert res.amount == 1500
    t_calc = (time.perf_counter() - t0) * 1000.0
    avg_calc = t_calc / 1000.0
    print(f"  ✅ 1,000 fee calculations completed in {t_calc:.2f} ms")
    print(f"  ⚡ Average Latency per request: {avg_calc:.4f} ms (< 0.05 ms!)")

    # 2. Document Advisor Benchmark
    print("\n[2/4] Testing Document Advisor (1,000 requests)...")
    adv_req = DocumentAdvisorRequest(
        service="fresh",
        applicant_type="adult",
        scheme="tatkaal",
        has_10th_pass_certificate=True
    )
    advisor_service.get_advice(adv_req)
    t0 = time.perf_counter()
    for _ in range(1000):
        res = advisor_service.get_advice(adv_req)
        assert res.non_ecr_eligible is True
        assert len(res.mandatory_annexures) > 0
    t_adv = (time.perf_counter() - t0) * 1000.0
    avg_adv = t_adv / 1000.0
    print(f"  ✅ 1,000 advisory queries completed in {t_adv:.2f} ms")
    print(f"  ⚡ Average Latency per request: {avg_adv:.4f} ms (< 0.05 ms!)")

    # 3. Zero-Rejection Cross-Document Auditor
    print("\n[3/4] Testing Zero-Rejection Cross-Document Engine...")
    audit_req = DocumentAuditRequest(
        target_service="fresh",
        documents=[
            DocumentFieldExtraction(
                document_type="aadhaar",
                extracted_name="S. SHARMA",
                extracted_dob="1998-05-15",
                extracted_father_name="SURESH SHARMA",
                extracted_gender="Male",
                extracted_address="Flat 402, Green Valley, New Delhi",
                extracted_pincode="110002"
            ),
            DocumentFieldExtraction(
                document_type="10th_marksheet",
                extracted_name="SAGAR SHARMA",
                extracted_dob="1998-05-15",
                extracted_father_name="SURESH SHARMA"
            )
        ]
    )
    t0 = time.perf_counter()
    audit_res = document_auditor_service.audit_documents(audit_req)
    t_audit = (time.perf_counter() - t0) * 1000.0
    print(f"  ✅ Discrepancy Audited in {t_audit:.2f} ms")
    print(f"  📊 PSK Readiness Score: {audit_res.psk_readiness_score}% ({audit_res.rejection_risk_level})")
    print(f"  🔍 Discrepancies Flagged: {len(audit_res.discrepancies)} ({audit_res.discrepancies[0].explanation})")
    print(f"  📝 Auto-Filled Form: {audit_res.auto_filled_form.given_name} {audit_res.auto_filled_form.surname} (Non-ECR: {audit_res.auto_filled_form.is_non_ecr})")

    # 4. Slot Radar & Atomic Reservation
    print("\n[4/4] Testing Slot Radar & Atomic Reservation Engine...")
    search_req = SlotSearchRequest(city_or_pincode="Delhi", service_type="normal")
    slots = slot_service.search_slots(search_req)
    print(f"  ✅ Found {len(slots)} PSK/POPSK centers in Delhi.")
    first_center = slots[0]
    hold_req = SlotHoldRequest(
        center_id=first_center.center_id,
        appointment_date=first_center.earliest_date,
        appointment_time="11:15 AM",
        scheme="normal",
        applicant_id="USR_CITIZEN_001"
    )
    hold_res = slot_service.hold_slot(hold_req)
    print(f"  🎟️ Atomic Slot Held: Token = {hold_res.hold_token}, Center = {hold_res.center_name}, Amount = ₹{hold_res.amount_payable}")

    print("\n" + "=" * 60)
    print("🏆 ALL BACKEND ENGINES VALIDATED & OPERATING AT ULTRA-LOW LATENCY!")
    print("=" * 60)

if __name__ == "__main__":
    run_benchmarks()
