# services/analyze_services.py
from supabase import Client
from typing import Any, Dict, List
from utils.history import add_to_history
from external.pipeline import pipeline  #

# Color mapping for SDG cards in the UI
SDG_COLORS = {
    1: "#e5243b",
    2: "#dda63a",
    3: "#4c9f38",
    4: "#c5192d",
    5: "#ff3a21",
    6: "#26bde2",
    7: "#fcc30b",
    8: "#a21942",
    9: "#fd6925",
    10: "#dd1367",
    11: "#fd9d24",
    12: "#bf8b2e",
    13: "#3f7e44",
    14: "#0a97d9",
    15: "#56c02b",
    16: "#00689d",
    17: "#19486a",
}


def _extract_labels_and_scores(raw: Any) -> tuple[list[str], list[float]]:
    """
    Try to handle the common HF pipeline output shapes and
    return (labels, scores).
    """
    labels: list[str] = []
    scores: list[float] = []

    # 1) dict: {"labels": [...], "scores": [...]}
    if isinstance(raw, dict):
        if "labels" in raw and "scores" in raw:
            labels = list(raw.get("labels") or [])
            scores = [float(s) for s in (raw.get("scores") or [])]

        # dict: single { "label": "...", "score": ... }
        elif "label" in raw and "score" in raw:
            labels = [str(raw["label"])]
            scores = [float(raw["score"])]

    # 2) list
    elif isinstance(raw, list) and raw:
        first = raw[0]

        # pattern: [{"labels": [...], "scores": [...]}, ...]
        if isinstance(first, dict) and "labels" in first and "scores" in first:
            labels = list(first.get("labels") or [])
            scores = [float(s) for s in (first.get("scores") or [])]

        # pattern: [{"label": "...", "score": ...}, ...]
        elif isinstance(first, dict) and "label" in first and "score" in first:
            labels = [str(item.get("label", "")) for item in raw]
            scores = [float(item.get("score", 0.0)) for item in raw]

    return labels, scores


class AnalyzeServices:
    @staticmethod
    def analyze_text(db: Client, text: str, uid: Optional[str]) -> Dict[str, Any]:
        # 1) Call external pipeline
        raw = pipeline(text)
        print("PIPELINE RAW RESPONSE:", raw)

        # 2) Normalize to labels + scores
        labels, scores = _extract_labels_and_scores(raw)

        detected_sdgs: List[Dict[str, Any]] = []

        # Only proceed if we actually got labels
        if labels:
            for label, score in list(zip(labels, scores))[:3]:
                sdg_id = None
                name = label

                try:
                    if ": " in label:
                        left, right = label.split(": ", 1)
                        name = right
                    else:
                        left = label

                    if " " in left:
                        _, num_str = left.split(" ", 1)
                        sdg_id = int(num_str)
                except Exception:
                    sdg_id = None
                    name = label

                detected_sdgs.append(
                    {
                        "id": sdg_id,
                        "name": name,
                        "percentage": round(float(score) * 100),
                        "color": SDG_COLORS.get(sdg_id, "#2e7d32"),
                    }
                )

        # 3) Build summary string
        if detected_sdgs:
            summary = (
                "The analysis detected the following most relevant SDGs: "
                + ", ".join(
                    (
                        f"SDG {item['id']} {item['name']} ({item['percentage']}%)"
                        if item["id"] is not None
                        else f"{item['name']} ({item['percentage']}%)"
                    )
                    for item in detected_sdgs
                )
            )
        else:
            summary = (
                "No specific SDGs could be confidently detected from the provided text."
            )

        result: Dict[str, Any] = {
            "detectedSDGs": detected_sdgs,
            "summary": summary,
            "raw": raw,
            "text": text,
        }

        # 4) Save to history ONLY if we have a user id
        if uid:
            add_to_history(db, uid, text, result)

        return result

    @staticmethod
    def get_history(db: Client, user_id: str):
        res = (
            db.table("history")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        return res.data or []