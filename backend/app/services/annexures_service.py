import json
import os
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class AnnexureDetail(BaseModel):
    code: str
    title: str
    category: str
    purpose: str
    template: str
    required_fields: List[str]

class GeneratedAnnexureResponse(BaseModel):
    code: str
    title: str
    category: str
    legal_text: str
    is_ready_for_print: bool
    missing_fields: List[str]

class AnnexuresService:
    def __init__(self):
        self.annexures: List[Dict[str, Any]] = []
        self._load_catalog()

    def _load_catalog(self):
        file_path = os.path.join(os.path.dirname(__file__), "..", "data", "annexures_catalog.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.annexures = json.load(f).get("annexures", [])
        except Exception as e:
            print(f"Warning: Could not load annexures_catalog.json: {e}")
            self.annexures = []

    def list_all(self, category: Optional[str] = None) -> List[AnnexureDetail]:
        res = []
        for a in self.annexures:
            if category and a["category"].lower() != category.lower():
                continue
            res.append(AnnexureDetail(**a))
        return res

    def get_by_code(self, code: str) -> Optional[AnnexureDetail]:
        matched = next((a for a in self.annexures if a["code"].upper() == code.upper()), None)
        return AnnexureDetail(**matched) if matched else None

    def generate_affidavit(self, code: str, user_data: Dict[str, Any]) -> GeneratedAnnexureResponse:
        ann = self.get_by_code(code)
        if not ann:
            raise ValueError(f"Annexure code '{code}' not found in official MEA catalog.")

        template_text = ann.template
        missing: List[str] = []

        # Replace fields
        for field in ann.required_fields:
            val = user_data.get(field)
            if val is not None and str(val).strip():
                template_text = template_text.replace(f"{{{field}}}", str(val).strip())
            else:
                template_text = template_text.replace(f"{{{field}}}", f"[{field.upper()}]")
                missing.append(field)

        return GeneratedAnnexureResponse(
            code=ann.code,
            title=ann.title,
            category=ann.category,
            legal_text=template_text,
            is_ready_for_print=len(missing) == 0,
            missing_fields=missing
        )

annexures_service = AnnexuresService()
