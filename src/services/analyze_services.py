# services/analyze_services.py
from external.pipeline import pipeline
from supabase import Client
from utils.history import add_to_history

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


class AnalyzeServices:
    @staticmethod
    def analyze_text(db: Client, text: str, uid: str) -> dict:
        # Call external Hugging Face pipeline
        response = pipeline(text)

        # 🔍 TEMP: print raw response in backend logs so you can inspect it
        print("PIPELINE RAW RESPONSE:", response)

        labels: list[str] = []
        scores: list[float] = []

        # --- CASE 1: zero-shot classification: [{"labels": [...], "scores": [...], ...}]
        if isinstance(response, list) and len(response) > 0 and isinstance(response[0], dict):
            first = response[0]
            if "labels" in first and "scores" in first:
                labels = first.get("labels", [])
                scores = first.get("scores", [])

        # --- CASE 2: list of {"label": "...", "score": ...}
        if not labels and isinstance(response, list) and len(response) > 0:
            maybe_label_scores = response
            if isinstance(maybe_label_scores[0], dict) and "label" in maybe_label_scores[0]:
                labels = [item.get("label", "") for item in maybe_label_scores]
                scores = [item.get("score", 0.0) for item in maybe_label_scores]

        detected_sdgs = []

        # Only proceed if we actually got labels
        if labels:
            # Take top 3
            for label, score in list(zip(labels, scores))[:3]:
                # Expected format: "SDG 13: Climate Action" or just "SDG 13"
                sdg_id = None
                name = label
                try:
                    if ": " in label:
                        left, right = label.split(": ", 1)         # "SDG 13", "Climate Action"
                        name = right
                    else:
                        left = label                              # "SDG 13"

                    if " " in left:
                        _, num_str = left.split(" ", 1)          # "SDG", "13"
                        sdg_id = int(num_str)
                except Exception:
                    # If parsing fails, leave id as None and name as full label
                    sdg_id = None
                    name = label

                detected_sdgs.append(
                    {
                        "id": sdg_id,
                        "name": name,
                        "percentage": round(score * 100),
                        "color": SDG_COLORS.get(sdg_id, "#2e7d32"),
                    }
                )

        if detected_sdgs:
            summary = (
                "The analysis detected the following most relevant SDGs: "
                + ", ".join(
                    f"SDG {item['id']} {item['name']} ({item['percentage']}%)"
                    if item["id"] is not None
                    else f"{item['name']} ({item['percentage']}%)"
                    for item in detected_sdgs
                )
            )
        else:
            summary = "No specific SDGs could be confidently detected from the provided text."

        results = {
            "detectedSDGs": detected_sdgs,
            "summary": summary,
        }

        add_to_history(db, uid, text, results)
        
        return results

    @staticmethod
    def get_history(db: Client):
        response = db.table("history").select("*").execute()
        return response