from external.pipeline import pipeline

class AnalyzeServices:
    @staticmethod
    def analyze_text(text: str):
        response = pipeline(text)
        return response[:3]