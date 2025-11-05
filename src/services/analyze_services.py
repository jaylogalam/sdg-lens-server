class AnalyzeServices:
    @staticmethod
    def analyze_text(text: str):
        keywords = {
            "poverty": "SDG 1: No Poverty",
            "hunger": "SDG 2: Zero Hunger",
            "education": "SDG 4: Quality Education",
            "energy": "SDG 7: Affordable and Clean Energy",
            "climate": "SDG 13: Climate Action",
        }

        matched = []  
        lower_text = text.lower()

        for keyword, sdg in keywords.items():
            if keyword in lower_text:
                matched.append({"keyword": keyword, "sdg": sdg})

        if not matched:
            matched.append({"keyword": None, "sdg": "No related SDG found."})

        # Return a clean JSON-like structure
        return {
            "matched_count": len(matched),
            "matches": matched
        }
