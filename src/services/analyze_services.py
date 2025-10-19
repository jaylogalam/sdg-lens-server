from transformers import pipeline # type: ignore
from transformers import ZeroShotClassificationPipeline
from typing import Dict

class AnalyzeServices:
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
        "SDG 17: Partnerships for the Goals"
    ]
    
    @classmethod
    def analyze_text(
        cls,
        classifier: ZeroShotClassificationPipeline,
        text_input: str
    ):
        results = classifier( # type: ignore
            text_input, 
            candidate_labels=cls.labels, 
            multi_label=True
        )

        labeled_scores = list(zip(results['labels'], results['scores'])) # type: ignore
        labeled_scores.sort(key=lambda item: item[1], reverse=True)

        response: Dict[str, Dict[str, str]] = {}
        
        for index, (label, score) in enumerate(labeled_scores[:3]):
            response[str(index + 1)] = {
                'label': str(label),
                'score': str(f"{score:.4f}")
            }

        return response