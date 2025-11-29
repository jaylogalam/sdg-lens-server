# services/pipeline.py (example path)
from core.secrets import PIPELINE_URL, PIPELINE_KEY
from typing import Any, Dict
import requests

if not PIPELINE_URL or not PIPELINE_KEY:
    raise ValueError("PIPELINE_URL or PIPELINE_KEY is not set")

headers = {
    "Authorization": f"Bearer {PIPELINE_KEY}",
}

labels: list[str] = [
    "SDG 1: No Poverty",
    "SDG 2: Zero Hunger",
    "SDG 3: Good Health and Well-being",
    "SDG 4: Quality Education",
    "SDG 5: Gender Equality",
    "SDG 6: Clean Water and Sanitation",
    "SDG 7: Affordable and Clean Energy",
    "SDG 8: Decent Work and Economic Growth",
    "SDG 9: Industry, Innovation, and Infrastructure",
    "SDG 10: Reduced Inequalities",
    "SDG 11: Sustainable Cities and Communities",
    "SDG 12: Responsible Consumption and Production",
    "SDG 13: Climate Action",
    "SDG 14: Life Below Water",
    "SDG 15: Life on Land",
    "SDG 16: Peace, Justice, and Strong Institutions",
    "SDG 17: Partnerships for the Goals",
]


def build_payload(text: str) -> Dict[str, Any]:
    return {
        "inputs": text,
        "parameters": {
            "candidate_labels": labels,
        },
    }


def pipeline(text: str) -> Dict[str, Any]:
    try:
        response = requests.post(
            PIPELINE_URL,
            headers=headers,
            json=build_payload(text),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Pipeline call failed: {e}")
