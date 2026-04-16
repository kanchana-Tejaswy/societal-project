import io
import numpy as np
from PIL import Image, UnidentifiedImageError

# ----------------------------------------------------
# 1. CONFIG
# ----------------------------------------------------
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# ----------------------------------------------------
# 2. FILE VALIDATION
# ----------------------------------------------------
def allowed_file(filename: str) -> bool:
    """
    Check if uploaded file has valid image extension.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ----------------------------------------------------
# 3. IMAGE PROCESSING FOR CNN
# ----------------------------------------------------
def process_image_for_cnn(image_bytes, filename=""):
    """
    Converts raw image bytes into a normalized tensor
    suitable for MobileNetV2 CNN inference.
    """

    # Validate file extension
    if filename and not allowed_file(filename):
        return {
            "valid": False,
            "error": "Only JPG, JPEG, PNG files are allowed."
        }

    try:
        # Load image from memory
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Resize for MobileNetV2
        img = img.resize((224, 224))

        # Convert to numpy array
        img_array = np.array(img, dtype=np.float32)

        # Normalize pixel values (0-1)
        img_array = img_array / 255.0

        # Add batch dimension -> (1, 224, 224, 3)
        img_array = np.expand_dims(img_array, axis=0)

        return {
            "valid": True,
            "tensor": img_array
        }

    except UnidentifiedImageError:
        return {
            "valid": False,
            "error": "Invalid or corrupted image file."
        }

    except Exception as e:
        return {
            "valid": False,
            "error": f"Image processing failed: {str(e)}"
        }