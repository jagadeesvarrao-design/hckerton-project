import time
import pytest
from app.services.calculator_service import calculator_service
from app.services.advisor_service import advisor_service
from app.models.schemas import FeeCalculationRequest, DocumentAdvisorRequest

def test_calculator_sub_millisecond_latency():
    """Verify that fee calculation operates in sub-millisecond speeds (<1.0ms)"""
    req = FeeCalculationRequest(
        service="fresh",
        applicant_age_group="adult",
        booklet_pages=36,
        scheme="normal",
        validity_years=10
    )
    
    # Warm up cache
    calculator_service.calculate_fee(req)
    
    # Measure 1,000 iterations for concurrency simulation
    start = time.perf_counter()
    for _ in range(1000):
        resp = calculator_service.calculate_fee(req)
        assert resp.amount == 1500
    
    total_elapsed = time.perf_counter() - start
    avg_latency_ms = (total_elapsed / 1000.0) * 1000.0
    print(f"\n⚡ Average Calculator Latency across 1,000 requests: {avg_latency_ms:.4f} ms")
    assert avg_latency_ms < 1.0, f"Latency {avg_latency_ms} ms exceeded 1ms threshold"

def test_advisor_sub_millisecond_latency():
    """Verify that document advisor operates in sub-millisecond speeds (<1.0ms)"""
    req = DocumentAdvisorRequest(
        service="fresh",
        applicant_type="adult",
        scheme="tatkaal",
        has_10th_pass_certificate=True
    )
    
    # Warm up cache
    advisor_service.get_advice(req)
    
    start = time.perf_counter()
    for _ in range(1000):
        resp = advisor_service.get_advice(req)
        assert resp.non_ecr_eligible is True
        assert len(resp.mandatory_annexures) > 0 # Annexure E for Tatkaal
    
    total_elapsed = time.perf_counter() - start
    avg_latency_ms = (total_elapsed / 1000.0) * 1000.0
    print(f"\n⚡ Average Advisor Latency across 1,000 requests: {avg_latency_ms:.4f} ms")
    assert avg_latency_ms < 1.0
