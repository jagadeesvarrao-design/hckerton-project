import json
import os
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.core.cache import cache

class PoliceStationInfo(BaseModel):
    thana_code: str
    thana_name: str
    sho_name: str
    contact: str
    address: str
    pincodes: List[str]
    district: str
    state: str

class PoliceStationService:
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self._load_data()

    def _load_data(self):
        file_path = os.path.join(os.path.dirname(__file__), "..", "data", "police_stations.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.data = json.load(f).get("states", {})
        except Exception as e:
            print(f"Warning: Could not load police_stations.json: {e}")
            self.data = {}

    def list_states(self) -> List[str]:
        return sorted(list(self.data.keys()))

    def list_districts(self, state: str) -> List[str]:
        st = self.data.get(state)
        if not st:
            return []
        return sorted(list(st.get("districts", {}).keys()))

    def locate_stations(self, state: Optional[str] = None, district: Optional[str] = None, pincode: Optional[str] = None) -> List[PoliceStationInfo]:
        results: List[PoliceStationInfo] = []
        
        # If pincode provided, search globally across all states/districts
        if pincode:
            p_clean = pincode.strip()
            for s_name, s_data in self.data.items():
                for d_name, thanas in s_data.get("districts", {}).items():
                    for t in thanas:
                        if p_clean in t.get("pincodes", []):
                            results.append(PoliceStationInfo(
                                thana_code=t["thana_code"],
                                thana_name=t["thana_name"],
                                sho_name=t["sho_name"],
                                contact=t["contact"],
                                address=t["address"],
                                pincodes=t["pincodes"],
                                district=d_name,
                                state=s_name
                            ))
            if results:
                return results

        # Filter by State and District
        if state and state in self.data:
            s_data = self.data[state]
            if district and district in s_data.get("districts", {}):
                thanas = s_data["districts"][district]
                for t in thanas:
                    results.append(PoliceStationInfo(
                        thana_code=t["thana_code"],
                        thana_name=t["thana_name"],
                        sho_name=t["sho_name"],
                        contact=t["contact"],
                        address=t["address"],
                        pincodes=t["pincodes"],
                        district=district,
                        state=state
                    ))
            else:
                for d_name, thanas in s_data.get("districts", {}).items():
                    for t in thanas:
                        results.append(PoliceStationInfo(
                            thana_code=t["thana_code"],
                            thana_name=t["thana_name"],
                            sho_name=t["sho_name"],
                            contact=t["contact"],
                            address=t["address"],
                            pincodes=t["pincodes"],
                            district=d_name,
                            state=state
                        ))

        return results

police_station_service = PoliceStationService()
