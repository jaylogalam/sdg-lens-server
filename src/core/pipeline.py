from transformers import pipeline, ZeroShotClassificationPipeline
from functools import lru_cache

class Pipeline:
    @staticmethod
    @lru_cache(maxsize=1)
    def get_classifier() -> ZeroShotClassificationPipeline:
        """Initializes and caches the heavy zero-shot classification model."""
        print("Loading zero-shot classification model... (This runs only once)")
        # The return type of this function is explicitly Pipeline
        classifier = pipeline(
            "zero-shot-classification", 
            model="facebook/bart-large-mnli",
            token=None
        )
        
        return classifier