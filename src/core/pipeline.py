from transformers import pipeline

classifier_model = None 

class Pipeline:
    @staticmethod
    async def load_classifier_model():
        """Initializes the heavy model globally."""
        print("Explicitly loading zero-shot classification model ONCE via startup event...")
        global classifier_model
        
        # Check if the model is already loaded (useful if this function is called multiple times by accident)
        if classifier_model is None:
            classifier_model = pipeline(
                "zero-shot-classification", 
                model="MoritzLaurer/xtremedistil-l6-h256-zeroshot-v1.1-all-33",
                token=None
            )
            print("Model loading complete.")
        else:
            print("Model already loaded.")
    
    @staticmethod
    def get_classifier():
        global classifier_model
        
        if classifier_model is None:
            raise RuntimeError("Classifier model not yet loaded via startup event.")
        
        return classifier_model