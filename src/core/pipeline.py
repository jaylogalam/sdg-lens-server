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
            model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0",
            token=None
        )
        
        return classifier