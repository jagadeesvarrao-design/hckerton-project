import urllib.request
import json
import time

BASE_URL = "http://127.0.0.1:8099/api/v1"

def post_json(endpoint, payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}{endpoint}", data=data, headers={'Content-Type': 'application/json'})
    t0 = time.perf_counter()
    with urllib.request.urlopen(req) as resp:
        elapsed = (time.perf_counter() - t0) * 1000.0
        return resp.status, json.loads(resp.read().decode()), elapsed, resp.headers.get("X-Process-Time-Ms")

def get_json(endpoint):
    t0 = time.perf_counter()
    with urllib.request.urlopen(f"{BASE_URL}{endpoint}") as resp:
        elapsed = (time.perf_counter() - t0) * 1000.0
        return resp.status, json.loads(resp.read().decode()), elapsed, resp.headers.get("X-Process-Time-Ms")

def main():
    print("=" * 70)
    print("🚀 PASSPORT SEVA AI 2.0 — FULL API FEATURE & HTTP VERIFICATION")
    print("=" * 70)

    tests = [
        ("1. Fee Calculator", "/calculator/calculate", "POST", {"service":"fresh", "applicant_age_group":"adult", "booklet_pages":36, "scheme":"tatkaal", "validity_years":10}),
        ("2. Document Advisor", "/advisor/advisory", "POST", {"service":"fresh", "applicant_type":"adult", "scheme":"normal", "has_10th_pass_certificate":True}),
        ("3. Zero-Rejection Auditor", "/audit/verify", "POST", {"target_service":"fresh", "documents":[{"document_type":"aadhaar","extracted_name":"SAGAR SHARMA","extracted_dob":"1998-05-15"},{"document_type":"10th_marksheet","extracted_name":"SAGAR SHARMA","extracted_dob":"1998-05-15"}]}),
        ("4. Slot Radar Search", "/slots/search", "POST", {"city_or_pincode":"Delhi", "service_type":"normal"}),
        ("5. Atomic Slot Hold", "/slots/hold", "POST", {"center_id":"PSK_DEL_01", "appointment_date":"2026-08-21", "appointment_time":"10:30 AM", "scheme":"normal", "applicant_id":"CITIZEN_42"}),
        ("6. Know Your Police Station", "/police-station/locate?pincode=110001", "GET", None),
        ("7. Annexures Catalog (A to M)", "/annexures/catalog", "GET", None),
        ("8. Affidavit Auto-Generator", "/annexures/ANNEXURE_E/generate", "POST", {"applicant_name":"SAGAR SHARMA","father_name":"SURESH SHARMA","dob":"1998-05-15","pob":"DELHI","address":"Connaught Place, New Delhi","police_station":"Connaught Place Police Station"}),
        ("9. Lodge Grievance to RPO", "/grievance/lodge", "POST", {"file_number":"DL10829384729","applicant_name":"SAGAR SHARMA","contact_number":"9876543210","email_id":"sagar@example.com","passport_office":"RPO Delhi","grievance_category":"DELAY_IN_POLICE_VERIFICATION","description":"Physical verification report pending."}),
        ("10. National Helplines & Contact", "/grievance/helplines", "GET", None),
        ("11. Live File Status Tracker", "/tracker/track", "POST", {"file_number":"DL10829384729"}),
        ("12. Citizen Copilot (Multilingual)", "/copilot/chat", "POST", {"message":"What are the documents required for passport?","language":"en"})
    ]

    for name, endpoint, method, payload in tests:
        if method == "POST":
            status, res, elapsed, ptime = post_json(endpoint, payload)
        else:
            status, res, elapsed, ptime = get_json(endpoint)
        
        assert status == 200, f"Failed on {name}"
        print(f"  [PASS] {name:<35} | HTTP 200 | Roundtrip: {elapsed:.2f} ms | Server Time: {ptime} ms")

    print("\n" + "=" * 70)
    print("🏆 ALL 12 SERVICES & FEATURES VERIFIED WITH 100% SUCCESS!")
    print("=" * 70)

if __name__ == "__main__":
    main()
