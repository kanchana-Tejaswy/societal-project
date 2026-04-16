import os
import numpy as np
import logging

# -----------------------------
# LOGGING SETUP
# -----------------------------
logger = logging.getLogger(__name__)

# Reduce TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# -----------------------------
# LOAD CNN MODEL (ONCE)
# -----------------------------
model = None

try:
    from tensorflow.keras.models import load_model

    model_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "waste_cnn_model.h5"
    )

    if os.path.exists(model_path):
        model = load_model(model_path)
        logger.info("CNN model loaded successfully.")
    else:
        logger.warning("Model file not found: waste_cnn_model.h5")

except Exception as e:
    logger.warning(f"TensorFlow load failed: {e}")


# -----------------------------
# PREDICTION FUNCTION
# -----------------------------
def evaluate_waste_cnn(image_tensor):
    """
    Returns:
    (predicted_class, confidence_percentage)
    """

    if image_tensor is None:
        return "Unknown", 0.0

    if model is None:
        return "No Model", 0.0

    try:
        # Predict
        prediction = model.predict(image_tensor, verbose=0)

        # Safety check
        if prediction is None or len(prediction) == 0:
            return "Invalid Output", 0.0

        class_index = int(np.argmax(prediction[0]))
        confidence = float(prediction[0][class_index]) * 100

        classes = ["glass", "metal", "paper", "plastic"]

        if class_index < 0 or class_index >= len(classes):
            return "Unknown", confidence

        return classes[class_index].capitalize(), confidence

    except Exception as e:
        logger.error(f"CNN prediction error: {e}")
        return "Inference Error", 0.0