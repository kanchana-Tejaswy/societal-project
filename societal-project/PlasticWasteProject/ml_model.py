import numpy as np
import os
import logging

# Limit TensorFlow verbosity preventing standard container log explosions
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

logger = logging.getLogger(__name__)

# GLOBAL CACHE LOAD: Heavily resolves HTTP Latency crashes by instantiating weight loads ONCE on startup natively securely.
model = None
try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "waste_cnn_model.h5")
    
    if os.path.exists(model_path):
        model = load_model(model_path)
        logger.info("Deep CNN Matrix Weights Synced Natively.")
    else:
        logger.warning("CNN Execution Engine Unavailable: .h5 compile missing.")
except Exception as e:
    logger.error(f"Global Inference Pipeline Corrupted natively: {e}")

def evaluate_waste_cnn(image_tensor):
    """
    Native Execution Inference natively bypassing generic latency cleanly parsing confidence structures stably.
    Returns: Tuple(Predicted_Class, Confidence_Percentage)
    """
    if image_tensor is None:
        return "Unknown Execution Matrix", 0.0

    # Strict Categorical Sorting matching identically flow_from_directory boundaries safely
    classes = ["glass", "metal", "paper", "plastic"]

    if model:
        try:
            # Native Deep Learning predictions mapped securely outputting confidence array percentages natively
            prediction = model.predict(image_tensor, verbose=0)
            class_index = np.argmax(prediction[0])
            confidence = float(prediction[0][class_index]) * 100.0
            predicted_class = classes[class_index].capitalize()
            
            logger.info(f"SUCCESS Mapped: {predicted_class} ({confidence:.2f}%)")
            
            return predicted_class, confidence

        except Exception as e:
            logger.error(f"CNN Predict Error Triggered: {e}")
            return "Inference Crash", 0.0

    return "No Model (.h5) Executing Native Fallback", 0.0