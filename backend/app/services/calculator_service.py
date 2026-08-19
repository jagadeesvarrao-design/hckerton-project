import json
import os
import time
from typing import Dict, Any, List
from app.models.schemas import FeeCalculationRequest, FeeCalculationResponse
from app.core.cache import cache

class CalculatorService:
    def __init__(self):
        self.rules: List[Dict[str, Any]] = []
        self._load_matrix()

    def _load_matrix(self):
        file_path = os.path.join(os.path.dirname(__file__), "..", "data", "fee_matrix.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.rules = data.get("rules", [])
        except Exception as e:
            print(f"Warning: Could not load fee_matrix.json: {e}")
            self.rules = []

    def calculate_fee(self, req: FeeCalculationRequest) -> FeeCalculationResponse:
        start_time = time.perf_counter()
        
        # Cache Key Generation
        cache_key = f"fee_{req.service}_{req.applicant_age_group}_{req.booklet_pages}_{req.scheme}_{req.validity_years}_{req.reason}"
        cached = cache.get(cache_key)
        if cached:
            elapsed = (time.perf_counter() - start_time) * 1000.0
            cached_resp = FeeCalculationResponse(**cached)
            cached_resp.calculation_latency_ms = round(elapsed, 3)
            return cached_resp

        # Rule evaluation
        matched_rule = None
        for rule in self.rules:
            if rule.get("service") != req.service:
                continue
            if rule.get("applicant_age_group") and rule.get("applicant_age_group") != req.applicant_age_group:
                continue
            if rule.get("booklet_pages") and rule.get("booklet_pages") != req.booklet_pages:
                continue
            if rule.get("scheme") and rule.get("scheme") != req.scheme:
                continue
            if req.service == "reissue" and rule.get("reason") and rule.get("reason") != req.reason:
                continue
            
            matched_rule = rule
            break

        # Fallback default pricing if edge-case
        if not matched_rule:
            if req.service == "pcc":
                amount = 500
                desc = "Police Clearance Certificate (PCC) Application"
            elif req.service == "surrender":
                amount = 5000
                desc = "Surrender Certificate Application"
            elif req.scheme == "tatkaal":
                amount = 3500
                desc = f"{req.service.title()} Passport ({req.booklet_pages} Pages, Tatkaal Scheme)"
            else:
                amount = 1500 if req.booklet_pages == 36 else 2000
                desc = f"{req.service.title()} Passport ({req.booklet_pages} Pages, Normal Scheme)"
        else:
            amount = matched_rule["amount"]
            desc = matched_rule["description"]

        tatkaal_surcharge = 2000 if req.scheme == "tatkaal" else 0
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        resp_dict = {
            "service": req.service,
            "scheme": req.scheme,
            "amount": amount,
            "currency": "INR",
            "description": desc,
            "tatkaal_surcharge": tatkaal_surcharge,
            "calculation_latency_ms": round(elapsed_ms, 3)
        }

        # Cache response
        cache.set(cache_key, resp_dict, ttl=86400)
        return FeeCalculationResponse(**resp_dict)

calculator_service = CalculatorService()
